from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from proj.rss_views import RssFeed, AtomFeed
from proj.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),

        url('^$', index),

        url(r'^admin/', include(admin.site.urls)),

        url('^source/(?P<url>.+)', viewSource),
        url('^rename/(?P<word>\w+)/(?P<new>\w+)', renameWord),

        url('^(?P<word>\w+)/rss', RssFeed()),
        #url('^(?P<word>\w+)/atom', AtomFeed()),
        url('^(?P<word>\w+)/html', ajax),
        url('^(?P<word>\w+)/ajax', ajax),

        url('^(?P<word>\w+)/del/(?P<url>.+)', delSource),
        url('^(?P<word>\w+)/add/(?P<url>.+)', addSource),
        url('^(?P<word>\w+)/filter/(?P<regex>.*)', saveFilter),

        url('^(?P<word>\w+)/', index),
)
