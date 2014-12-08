# coding=utf-8
# Date: 14/12/8
# Time: 13:55
# Email:fanjunwei003@163.com
from django.db import models
import time

__author__ = u'范俊伟'


class DBCollection(models.Model):
    """Table of collections."""
    __tablename__ = "collection"

    path = models.CharField(max_length=200, primary_key=True)
    parent_path = models.CharField(max_length=200)


class DBItem(models.Model):
    """Table of collection's items."""
    __tablename__ = "item"

    name = models.CharField(max_length=200, primary_key=True)
    tag = models.TextField(max_length=255)
    collection = models.ForeignKey(DBCollection)


class DBHeader(models.Model):
    """Table of item's headers."""
    __tablename__ = "header"

    name = models.CharField(max_length=200)
    value = models.TextField(max_length=255)
    collection = models.ForeignKey(DBCollection)

    class Meta:
        unique_together = (("name", "collection"),)


class DBLine(models.Model):
    """Table of item's lines."""
    __tablename__ = "line"
    timestamp = models.IntegerField(default=lambda: time.time() * 10 ** 6, primary_key=True)
    name = models.TextField(max_length=255)
    value = models.TextField(max_length=255)
    item_name = models.ForeignKey(DBItem)


class DBProperty(models.Model):
    """Table of collection's properties."""
    __tablename__ = "property"

    name = models.CharField(max_length=200)
    value = models.TextField(max_length=255)
    collection = models.ForeignKey(DBCollection)

    class Meta:
        unique_together = (("name", "collection"),)