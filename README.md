django CalDAV 服务
=============
所需包
pip install django-ical
pip install lxml
pip install djangorestframework
pip install mock
pip install http

INSTALLED_APPS加入
'our_calendar',
'django_caldav',


url加入
url(r'^calendar(?P<path>.*)$', logged_in_or_basicauth("calendar")(OurCalendarView.as_view())),

MIDDLEWARE_CLASSES 注掉如下功能
#'django.middleware.csrf.CsrfViewMiddleware',

账号使用的是django自带的用户认证

