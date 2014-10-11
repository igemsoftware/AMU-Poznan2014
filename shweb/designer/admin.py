from django.contrib import admin

from designer.models import DesignProcessModel


class DesignProcessAdmin(admin.ModelAdmin):
    readonly_fields = ("datetime_start", "datetime_finish")
    list_display = ('transcript', 'process_id', 'datetime_start', 'datetime_finish')

admin.site.register(DesignProcessModel, DesignProcessAdmin)
