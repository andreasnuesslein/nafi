
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from proj.collector import News

from proj.models import Source, Word

class RssFeed(Feed):
    title = "NaFi: Nachrichten Filter"
    link = "http://"+"TODO"
    description = "News filter. One feed to conglomerate and filter them all..    and in the darkness bind them."

    def get_object(self, request, word):
        self.word = word
        pass

    def items(self):
        word = Word.objects.get(name=self.word)
        sources = Source.objects.filter(word=word)
        news = News(sources, word.regex)
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

class AtomFeed(RssFeed):
    feed_type = Atom1Feed
    link = "/atom/"
    subtitle = RssFeed.description
