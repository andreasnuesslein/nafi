
import feedparser
import re
from datetime import datetime
from time import mktime
from proj.models import NewsContent, NewsEntry

""" Internet-fetching Unit """
class Newsprovider:
    def __init__(self, source, filters):
        self.source = source
        self.fetch()

        reg = re.compile("|".join([u.regex for u in filters]), re.I)
        self.filtered_entries = [entry for entry in self.entries() if entry.matches(reg)]



    def fetch(self):
        try:
            self.provider = NewsContent.objects.get(url = self.source)
        except:
            self.provider = NewsContent(url = self.source)
            self.provider.save()
            self.provider.checked_last = datetime(datetime.now().year,1,1,0,0)

        diff = (datetime.now() - self.provider.checked_last)
        print(diff)
        if diff.days <= 0 and diff.seconds <= 1800:
            print("ALREADY CHECKED: %s" % (self.source))
            #return

        print("REDO CHECKING: %s" % (self.source))


        """ actually fetch news """
        feed = feedparser.parse( self.source )
        print feed.entries[0].keys()
        #import ipdb;ipdb.set_trace()

        entries = [x for x in feed.entries if (  datetime.fromtimestamp(mktime(x.updated_parsed)) > self.provider.checked_last)]
        print entries
        for entry in entries:
            ne = NewsEntry(url=entry.link, title=entry.title, title_detail=entry.title_detail,
                    summary=entry.summary, summary_detail=entry.summary_detail,
                    updated=datetime.fromtimestamp(mktime(entry.updated_parsed)),
                    provider = self.provider)
            ne.save()

        self.provider.save()

        return

    def entries(self):
        x = NewsEntry.objects.filter(provider=self.provider)
        print x
        return x



""" News will walk through given sources and filter the messages accordingly """
class News:
    def __init__(self, sources, filters):
        self.entries = []
        for source in sources:
            f = Newsprovider(source.url,filters)
            self.entries += f.filtered_entries
