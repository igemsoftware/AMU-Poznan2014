"""
.. module:: shweb.designer
   :platform: Unix, Windows
   :synopsis: Module with admin site settings for user's accounts

"""
from django.contrib import admin

from designer.models import DesignProcessModel


class DesignProcessAdmin(admin.ModelAdmin):
    """It's responsible for proper design model data presentation on admin site.
    """
    readonly_fields = ("datetime_start",) #"datetime_finish")
    list_display = ('process_id', 'datetime_start', 'datetime_finish')

admin.site.register(DesignProcessModel, DesignProcessAdmin)
