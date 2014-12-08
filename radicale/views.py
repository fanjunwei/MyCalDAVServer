# coding=utf-8
# Date: 14/12/7
# Time: 21:19
# Email:fanjunwei003@163.com
from django.http import HttpResponse
from django.utils.decorators import classonlymethod, method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from djangodav.views import DavView
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


class RadicaleView(View):
    http_method_names = ['options', 'put', 'mkcol', 'head', 'get', 'delete', 'propfind', 'proppatch', 'copy', 'move',
                         'lock', 'unlock']

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        response = None

        def start_response(status_code, headers):
            response = HttpResponse()
            response.status_code = status_code

            for i in headers:
                response[i[0]] = i[1]

        content = app(request.META, start_response)
        if response:
            response.content = content
        return response

    def _allowed_methods(self):
        return [m.upper() for m in self.http_method_names]




