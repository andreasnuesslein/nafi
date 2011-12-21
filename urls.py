from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from feedfilter.proj.rss_views import RssFeed, AtomFeed
from feedfilter.proj.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        url('^$', index),

        url('^(?P<timestamp>\d+)/rss', RssFeed()),
        url('^(?P<timestamp>\d+)/atom', AtomFeed()),
        url('^(?P<timestamp>\d+)/html', ajax),
        url('^(?P<timestamp>\d+)/ajax', ajax),
        url('^(?P<timestamp>\d+)/validate', validate_sources),
        url('^(?P<timestamp>\d+)/', index),


    url(r'^admin/', include(admin.site.urls)),
)
