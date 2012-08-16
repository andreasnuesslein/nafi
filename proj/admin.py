from django.contrib import admin
from feedfilter.proj.models import *

class SourceAdmin(admin.ModelAdmin):
    pass
class WordAdmin(admin.ModelAdmin):
    pass
class NewsContentAdmin(admin.ModelAdmin):
    pass
class NewsEntryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Source, SourceAdmin)
admin.site.register(Word, WordAdmin)
admin.site.register(NewsContent, NewsContentAdmin)
admin.site.register(NewsEntry, NewsEntryAdmin)

