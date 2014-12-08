django CalDAV 服务
=============
> 此分支为将radicale改造为基于django

INSTALLED_APPS加入
-------------
'radicale',  

url加入
-------------
url(r'^(?P\<path\>.*)$', radicaleViewHandle),  

如果需要CalDAV的服务路径不为根目录,例如基于/caldav/,则url配置为:  
> url(r'^caldav(?P\<path\>.*)$', radicaleViewHandle),  

并修改radicale/config.py  
> "base_prefix": "/caldav/"

MIDDLEWARE_CLASSES 注掉如下功能
-------------
\#'django.middleware.csrf.CsrfViewMiddleware',


账号使用的是django自带的用户认证

