from django.contrib import admin
from .models import SliderImage
from .utils import AdminThumbnailMixin

class SliderAdmin(admin.ModelAdmin, AdminThumbnailMixin):
    list_display= ('thumbnail','is_visible')
    thumbnail_options = {'size': (100,100), 'crop': True}

admin.site.register(SliderImage,SliderAdmin)