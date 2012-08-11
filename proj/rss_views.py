
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from feedfilter.collector import News

from feedfilter.proj.models import Source, Filter

class RssFeed(Feed):
    title = "NaFi: Nachrichten Filter"
    link = "http://nafi.noova.de/"
    description = "Newsfeed Aggregator for GP|Bln"

    def get_object(self, request, timestamp):
        self.timestamp = timestamp
        pass

    def items(self):
        sources = Source.objects.filter(group=self.timestamp)
        filters = Filter.objects.filter(group=self.timestamp)
        news = News(sources, filters)
        return news.entries


    def item_link(self, item):
        return item.url

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        if 'summary' in dir(item):
            return item.summary
        if 'title_detail' in dir(item):
            return item.title_detail
        return item.title

    def item_pubdate(self, item):
        from datetime import datetime
        from time import mktime
        return item.updated
        #return datetime.fromtimestamp(mktime(item.updated))

class AtomFeed(RssFeed):
    feed_type = Atom1Feed
    link = "/atom/"
    subtitle = RssFeed.description
