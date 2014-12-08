# coding=utf-8
# Date: 14/12/8
# Time: 00:08
# Email:fanjunwei003@163.com


from django.contrib.auth import authenticate

__author__ = u'范俊伟'


def is_authenticated(user, password):
    if user and password:
        au = authenticate(username=user, password=password)
        if au is not None:
            if au.is_active:
                return user

    return False