from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect
from django.core.mail import send_mail


from contrib.shortcuts import render_to_response
from proj.models import Source, Word
from proj.collector import News

def index(request, word=None):
    if not word:
        import base64
        import random
        word = ""
        while True:
            word = base64.b64encode(str(100*random.random()))[:7]
            if not len(Word.objects.filter(name=word)):
                return HttpResponseRedirect("/"+word)


    wordobj = Word.objects.filter(name=word)
    if wordobj:
        wordobj = wordobj[0]
    else:
        wordobj = Word(name=word,regex="")


    sources = Source.objects.filter(word=wordobj)

    template = 'index.html'
    data = {'sources': sources, 'regex': wordobj.regex, 'word':wordobj.name}

    return render_to_response(request, template, data)


def delSource(request, word, url):
    try:
        word = Word.objects.get(name=word)
        s = Source.objects.filter(url=url,word=word)
        for source in s:
            source.delete()
        return HttpResponse("ok")
    except:
        pass
    return HttpResponseForbidden("test")

def addSource(request, word, url):
    try:
        if not (url.startswith("http://") or url.startswith("https://")):
            url = "http://" + url
        #import ipdb;ipdb.set_trace()
        (word,x) = Word.objects.get_or_create(name=word)
        if Source.objects.filter(url=url,word=word).exists():
            return HttpResponseForbidden("exists_already")

        import feedparser
        feed = feedparser.parse(url)
        if feed.status >= 400:
            #import ipdb;ipdb.set_trace()
            return HttpResponseForbidden("no rss/atom found")

        s = Source(url=url,word=word)
        s.save()
        return HttpResponse(s.url)
    except:
        pass
    #import ipdb;ipdb.set_trace()
    return HttpResponseForbidden("unknown error")

def saveFilter(request, word, regex):
    try:
        (word,x) = Word.objects.get_or_create(name=word)
        word.regex = regex
        word.save()
        return HttpResponse("ok")
    except:
        return HttpResponseForbidden("error")

def renameWord(request, word, new):
    try:
        w = Word.objects.get(name=word)
        w.name = new
        w.save()
        return HttpResponse("ok")
    except:
        return HttpResponseForbidden("error")

def viewSource(request, url):
    sources= Source.objects.filter(url=url)
    news = News(sources,"")
    data = {'news': news.entries}
    template = 'ajax.html'
    return render_to_response(request, template, data)


def ajax(request, word):
    word = Word.objects.get(name=word)
    sources = Source.objects.filter(word=word)
    #filters = Filter.objects.filter(group=timestamp)
    news = News(sources,word.regex)

    data = {'news': news.entries}
    template = 'ajax.html'
    return render_to_response(request, template, data)

