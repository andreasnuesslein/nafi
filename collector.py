
import feedparser
import re
from datetime import datetime
from time import mktime
from proj.models import NewsContent, NewsEntry

""" Internet-fetching Unit """
class Newsprovider:
    def __init__(self, source):
        self.source = source
        self.fetch()


    def fetch(self):
        print "fetching: %s" % self.source
        try:
            self.provider = NewsContent.objects.get(url = self.source)
        except:
            self.provider = NewsContent(url = self.source)
            self.provider.save()
            self.provider.checked_last = datetime(datetime.now().year,1,1,0,0)

        diff = (datetime.now() - self.provider.checked_last)
        if diff.days <= 0 and diff.seconds <= 1800:
            return

        """ actually fetch news """
        feed = feedparser.parse( self.source )
        if not feed.entries:
            self.provider.delete()
            return

        if not hasattr(feed.entries[0], 'updated_parsed') or feed.entries[0]['updated_parsed'] == None:
            NewsEntry.objects.filter(provider = self.provider).delete()
        else:
            feed.entries = [x for x in feed.entries if (  datetime.fromtimestamp(mktime(x.updated_parsed)) > self.provider.checked_last)]

        for entry in feed.entries:
            try:
                updated = datetime.fromtimestamp(mktime(entry.updated_parsed))
                if updated == None:
                    updated = datetime.now()
            except:
                updated = datetime.now()

            ne = NewsEntry(url=entry.link, title=entry.title, summary=entry.summary,
                    updated=updated,
                    provider = self.provider)
            print ne
            ne.save()

        self.provider.save()

        return

    def entries(self):
        return NewsEntry.objects.filter(provider=self.provider)


    def myfilter(self, regex):
        reg = re.compile(regex, re.I)
        return [entry for entry in self.entries() if entry.matches(reg)]



""" News will walk through given sources and filter the messages accordingly """
class News:
    def __init__(self, sources, regex):
        self.entries = []
        for source in sources:
            f = Newsprovider(source.url)
            self.entries += f.myfilter(regex)
