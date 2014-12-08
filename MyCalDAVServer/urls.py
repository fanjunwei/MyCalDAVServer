from django.conf.urls import patterns, include, url

from django.contrib import admin
from radicale.views import radicaleViewHandle

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'MyCalDAVServer.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       #url(r'^admin/', include(admin.site.urls)),
                       url(r'^caldav(?P<path>.*)$', radicaleViewHandle),
)
