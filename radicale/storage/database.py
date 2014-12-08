# -*- coding: utf-8 -*-
#
# This file is part of Radicale Server - Calendar Server
# Copyright © 2013 Guillaume Ayoub
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Radicale.  If not, see <http://www.gnu.org/licenses/>.

"""
SQLAlchemy storage backend.

"""

import time
from datetime import datetime
from contextlib import contextmanager

from sqlalchemy import create_engine, Column, Unicode, Integer, ForeignKey
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from .. import config

from radicale.models import *




# These are classes, not constants
# pylint: disable=C0103
from radicale import ical


class Collection(ical.Collection):
    """Collection stored in a database."""

    def __init__(self, path, principal=False):
        super(Collection, self).__init__(path, principal)

    def __del__(self):
        pass

    def _query(self, item_types):
        """Get collection's items matching ``item_types``."""
        item_objects = []
        for item_type in item_types:
            items = DBItem.objects.filter(collection=self._db_collection, tag=item_type.tag).order_by('name')
            for item in items:
                text = "\n".join(
                    "%s:%s" % (line.name, line.value) for line in item.dbline_set.all())
                item_objects.append(item_type(text, item.name))
        return item_objects

    @property
    def _modification_time(self):
        """Collection's last modification time."""
        line_query = DBLine.objects.filter(item__collection=self._db_collection).order_by('-timestamp')
        if line_query.count() > 0:
            timestamp = line_query[0].timestamp
        else:
            timestamp = None
        if timestamp:
            return datetime.fromtimestamp(float(timestamp) / 10 ** 6)
        else:
            return datetime.now()

    @property
    def _db_collection(self):
        """Collection's object mapped to the table line."""
        try:
            return DBCollection.objects.get(path=self.path)
        except:
            return None

    def write(self, headers=None, items=None):
        headers = headers or self.headers or (
            ical.Header("PRODID:-//Radicale//NONSGML Radicale Server//EN"),
            ical.Header("VERSION:%s" % self.version))
        items = items if items is not None else self.items

        if self._db_collection:
            self._db_collection.dbitem_set.all().delete()
            self._db_collection.dbheader_set.all().delete()
        else:
            db_collection = DBCollection()
            db_collection.path = self.path
            db_collection.parent_path = "/".join(self.path.split("/")[:-1])
            db_collection.save()

        for header in headers:
            db_header = DBHeader()
            db_header.name, db_header.value = header.text.split(":", 1)
            db_header.collection = self._db_collection
            db_header.save()

        for item in items:
            db_item = DBItem()
            db_item.name = item.name
            db_item.tag = item.tag
            db_item.collection = self._db_collection
            db_item.save()

            for line in ical.unfold(item.text):
                db_line = DBLine()
                db_line.name, db_line.value = line.split(":", 1)
                db_line.item = db_item
                db_line.save()

    def delete(self):
        self._db_collection.delete()

    @property
    def text(self):
        return ical.serialize(self.tag, self.headers, self.items)

    @property
    def etag(self):
        return '"%s"' % hash(self._modification_time)

    @property
    def headers(self):
        headers = DBHeader.objects.filter(collection=self._db_collection).order_by('name')
        return [
            ical.Header("%s:%s" % (header.name, header.value))
            for header in headers]

    @classmethod
    def children(cls, path):
        children = DBCollection.objects.filter(parent_path=path or "")
        collections = [cls(child.path) for child in children]
        return collections

    @classmethod
    def is_node(cls, path):
        if not path:
            return True

        result = DBCollection.objects.filter(parent_path=path or "").count() > 0
        return result

    @classmethod
    def is_leaf(cls, path):
        if not path:
            return False
        try:
            collection = DBCollection.objects.get(path=path)
            result = DBItem.objects.filter(collection=collection).count() > 0
        except:
            result = False
        return result

    @property
    def last_modified(self):
        return time.strftime(
            "%a, %d %b %Y %H:%M:%S +0000", self._modification_time.timetuple())

    @property
    @contextmanager
    def props(self):
        # On enter
        properties = {}
        db_properties = DBProperty.objects.filter(collection=self._db_collection)
        for prop in db_properties:
            properties[prop.name] = prop.value
        old_properties = properties.copy()
        yield properties
        # On exit
        if self._db_collection and old_properties != properties:
            db_properties.delete()
            for name, value in properties.items():
                prop = DBProperty()
                prop.name = name
                prop.value = value
                prop.collection = self._db_collection
                prop.save()

    @property
    def items(self):
        return self._query(
            (ical.Event, ical.Todo, ical.Journal, ical.Card, ical.Timezone))

    @property
    def components(self):
        return self._query((ical.Event, ical.Todo, ical.Journal, ical.Card))

    @property
    def events(self):
        return self._query((ical.Event,))

    @property
    def todos(self):
        return self._query((ical.Todo,))

    @property
    def journals(self):
        return self._query((ical.Journal,))

    @property
    def timezones(self):
        return self._query((ical.Timezone,))

    @property
    def cards(self):
        return self._query((ical.Card,))

    def save(self):
        """Save the text into the collection.

        This method is not used for databases.

        """
        pass
