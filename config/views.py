from django.http import HttpResponseRedirect, HttpResponse

from feedparse.contrib.shortcuts import render_to_response
from feedparse.config.models import Source, Filter
from feedparse.collector import News

from time import time

def index(request, timestamp=None):
    if request.method == 'POST':
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
        timestamp = Source.objects.order_by('-group')[0].group
        return HttpResponseRedirect('/%s/' %(timestamp))


    template = 'index.html'
    sources = Source.objects.filter(group=timestamp)
    filters = Filter.objects.filter(group=timestamp)

    data = {'sources': sources, 'filters': filters, 'timestamp':timestamp}
    return render_to_response(request, template, data)

def htmlrss(request, timestamp):
    sources = Source.objects.filter(group=timestamp)
    filters = Filter.objects.filter(group=timestamp)

    template = 'rss.html'
    news = News(sources,filters)
    data = {'news': news.entries}
    return render_to_response(request, template, data)

