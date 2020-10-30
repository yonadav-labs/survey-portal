from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import *

class InfractionTypeAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('name', 'points', 'enabled')
    search_fields = ('name',)
    list_filter = ('enabled',)


class InfractionAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('representative', 'type', 'date')
    list_filter = ('type',)


admin.site.register(Infraction, InfractionAdmin)
admin.site.register(InfractionType, InfractionTypeAdmin)
