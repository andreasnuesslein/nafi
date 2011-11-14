
import feedparser
import re

class Entry:
    def __init__(self, content):
        for key in content.keys():
            setattr(self, key, content[key])

    def __unicode__(self):
        return self.updated + " | "+ self.summary

class Feed:
    def __init__(self, source, filters):
        self.feed = feedparser.parse( source )
        self.entries = []
        reg = re.compile("|".join([x.regex for x in filters]), re.I)

        for i in self.feed.entries:
            if reg.search(dict_lin(i)):

                self.entries += [Entry(i)]


def dict_lin(mydict):
    string = unicode(mydict.title)
    string += unicode(mydict.title_detail)
    string += unicode(mydict.summary)
    return string

class News:

    def __init__(self, sources, filters):
        self.entries = []
        for source in sources:
            f = Feed(source.url,filters)
            self.entries += f.entries
