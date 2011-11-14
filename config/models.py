from django.db import models

class Source(models.Model):
    url = models.URLField()
    group = models.IntegerField()

    def __unicode__(self):
        return("%s: %s" %(self.group, self.url))

    def sane(self):
        if self.url == "":
            return False
        return True

class Filter(models.Model):
    regex = models.CharField(max_length=200)
    group = models.IntegerField()

    def __unicode__(self):
        return("%s: %s" %(self.group, self.regex))

    def sane(self):
        if self.regex == "":
            return False
        return True
