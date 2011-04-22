from __future__ import print_function

import feedparser
import re

class Entry:
    def __init__(self, content):
        for key in content.keys():
            setattr(self, key, content[key])

    def __unicode__(self):
        return self.updated + " | "+ self.summary
        #return(u"%s %s %s" %(self.updated, self.title, self.summary))


class Feed:
    def __init__(self, source):
        self.feed = feedparser.parse( source )
        self.entries = []
        for i in self.feed.entries:
            self.entries += [Entry(i)]
        print(unicode(self.entries[0]))
    def match(self,include):
        pass





news = "http://www.tagesschau.de/xml/rss2"
f1 = Feed(news)
f1.match('x')

#import ipdb; ipdb.set_trace()
