from django.db import models
from feedparser import parse

class Source(models.Model):
    url = models.URLField()
    group = models.IntegerField()

    def __unicode__(self):
        return("%s: %s" %(self.group, self.url))

    def sane(self):
        if self.url == "":
            return False
        return True

    def validate(self):
        print "validate: "+self.url
        feed = parse(self.url)
        try:
            keys = feed.entries[0].keys()
            if len(set(keys) & set(['summary_detail', 'title', 'summary', 'title_detail', 'link', 'updated_parsed'])) == 6:
                return (self.url, 1)
            return (self.url, keys)

        except:
            return (self.url, -1)

class Filter(models.Model):
    regex = models.CharField(max_length=200)
    group = models.IntegerField()

    def __unicode__(self):
        return("%s: %s" %(self.group, self.regex))

    def sane(self):
        if self.regex == "":
            return False
        return True

class NewsContent(models.Model):
    url = models.URLField()
    checked_last = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return("%s: %s" % (self.checked_last, self.url))

class NewsEntry(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=500)
    title_detail = models.CharField(max_length=1000, blank=True)
    summary = models.CharField(max_length=500)
    summary_detail = models.CharField(max_length=1000, blank=True)
    updated = models.DateTimeField()
    provider = models.ForeignKey(NewsContent)

    def __unicode__(self):
        return("%s: %s" %(self.updated, self.title))

    def matches(self, regex):
        searchthrough = unicode(self.title) + unicode(self.title_detail) + unicode(self.summary) + \
                unicode(self.summary_detail)

        if regex.search(searchthrough):
            return True
        return False
