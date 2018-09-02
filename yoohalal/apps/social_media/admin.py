from django.contrib import admin

from . import models


class LinkTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'is_visible', 'order_number' ]

admin.site.register(models.LinkType, LinkTypeAdmin)