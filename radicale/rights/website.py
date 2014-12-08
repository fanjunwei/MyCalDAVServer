# coding=utf-8
# Date: 14/12/8
# Time: 00:25
# Email:fanjunwei003@163.com

__author__ = u'范俊伟'


def authorized(user, collection, permission):
    if not user:
        return False
    else:
        return True