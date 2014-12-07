from django.conf.urls import patterns, include, url

from django.contrib import admin
from our_calendar.auth import logged_in_or_basicauth
from our_calendar.views import OurCalendarView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MyCalDAVServer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^calendar(?P<path>.*)$', logged_in_or_basicauth("calendar")(OurCalendarView.as_view())),
)
