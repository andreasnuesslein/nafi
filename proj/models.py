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
            if 'updated_parsed' in keys:
                return {'url':self.url, 'status':'green'}
            return {'url':self.url, 'status':'#bbbb00', 'msg':'updated missing.. not gonna archive'}

        except:
            return {'url':self.url, 'status':'red'}

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
    summary = models.CharField(max_length=500)
    updated = models.DateTimeField(blank=True)
    provider = models.ForeignKey(NewsContent)

    def __unicode__(self):
        return("%s: %s" %(self.updated, self.title))

    def matches(self, regex):
        searchthrough = unicode(self.title) + unicode(self.summary)

        if regex.search(searchthrough):
            return True
        return False
