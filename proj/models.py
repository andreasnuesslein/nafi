from django.db import models
from feedparser import parse

class Word(models.Model):
    name = models.CharField(max_length=100)
    regex = models.CharField(max_length=500)

    def __unicode__(self):
        return("%s (%s)" %(self.name,self.regex))


class Source(models.Model):
    url = models.URLField()
    word = models.ForeignKey('Word')

    def __unicode__(self):
        return("%s: %s" %(self.word, self.url))


class NewsContent(models.Model):
    url = models.URLField()
    checked_last = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return("%s: %s" % (self.checked_last, self.url))


class NewsEntry(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=500)
    summary = models.CharField(max_length=5000)
    updated = models.DateTimeField(blank=True)
    provider = models.ForeignKey(NewsContent)

    def __unicode__(self):
        return("%s: %s" %(self.updated, self.title))

    def matches(self, regex):
        searchthrough = unicode(self.title) + unicode(self.summary)
        if regex.search(searchthrough):
            return True
        return False
