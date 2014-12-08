django CalDAV 服务
=============
INSTALLED_APPS加入
-------------
'radicale',  

url加入
-------------
url(r'^(?P<path>.*)$', radicaleViewHandle),  

MIDDLEWARE_CLASSES 注掉如下功能
-------------
\#'django.middleware.csrf.CsrfViewMiddleware',


账号使用的是django自带的用户认证

