# coding=utf-8
# Date: 14/12/7
# Time: 21:19
# Email:fanjunwei003@163.com
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from radicale import Application

__author__ = u'范俊伟'

app = Application()


def radicaleViewHandle(request, *args, **kwargs):
    response = HttpResponse()

    def start_response(status_code, headers):
        try:
            status_code = int(status_code)
        except:
            try:
                status_code = int(status_code.split(' ')[0])
            except:
                pass

        response.status_code = status_code

        for i in headers:
            response[i[0]] = i[1]

    environ = dict(request.META)
    content = app(environ, start_response)
    if response:
        response.content = '\n'.join(content)
    return response




