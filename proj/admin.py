from django.contrib import admin
from feedparse.proj.models import *

class SourceAdmin(admin.ModelAdmin):
    pass
class FilterAdmin(admin.ModelAdmin):
    pass

admin.site.register(Source, SourceAdmin)
admin.site.register(Filter, FilterAdmin)

