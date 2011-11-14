from django.conf.urls.defaults import patterns, include, url

from feedparse.feeds import RssFeed, AtomFeed
from feedparse.config.views import index, htmlrss

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        url('^$', index),

        url('^(?P<timestamp>\d+)/rss/', RssFeed()),
        url('^(?P<timestamp>\d+)/atom/', AtomFeed()),
        url('^(?P<timestamp>\d+)/html/', htmlrss),
        url('^(?P<timestamp>\d+)/', index),


    url(r'^admin/', include(admin.site.urls)),
)
