from django.http import HttpResponseRedirect, HttpResponse

from feedparse.contrib.shortcuts import render_to_response
from feedparse.proj.models import Source, Filter
from feedparse.collector import News

from time import time

def index(request, timestamp=None):
    validate = False
    print request.method
    if request.method == 'POST':
        if request.POST['op'] == "Validieren":
            timestamp = request.META['HTTP_REFERER'].split('/')[-2]
            return HttpResponseRedirect('/%s/validate/' %(timestamp))

        group = int(time())
        sources = request.POST['sources'].split('\r\n')
        filters = request.POST['filters'].split('\r\n')

        for source in sources:
            s = Source(url=source,group=group)
            if s.sane():
                s.save()
        for filt in filters:
            f = Filter(regex=filt,group=group)
            if f.sane():
                f.save()

        return HttpResponseRedirect('/%s/' %(group))


    if not timestamp:
        try:
            timestamp = Source.objects.order_by('-group')[0].group
        except:
            timestamp = 0
        return HttpResponseRedirect('/%s/' %(timestamp))


    sources = Source.objects.filter(group=timestamp)
    filters = Filter.objects.filter(group=timestamp)


    template = 'index.html'
    data = {'sources': sources, 'filters': filters, 'timestamp':timestamp}
    if validate:
        template = 'validate.html'
        data = {'sources': [ source.validate() for source in sources ] }


    return render_to_response(request, template, data)

def validate_sources(request, timestamp):
    sources = Source.objects.filter(group=timestamp)
    template = 'validate.html'
    valid_sources = [ source.validate() for source in sources ]
    data = {'sources': valid_sources }
    return render_to_response(request, template, data)


def htmlrss(request, timestamp):
    sources = Source.objects.filter(group=timestamp)
    filters = Filter.objects.filter(group=timestamp)

    template = 'rss.html'
    news = News(sources,filters)
    data = {'news': news.entries}
    return render_to_response(request, template, data)

