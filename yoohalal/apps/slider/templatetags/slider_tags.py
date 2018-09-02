from django import template
from apps.slider.models import SliderImage
register = template.Library()

@register.assignment_tag
def get_slider_images(limit=False, randomize=True, slider_number=1):

    qs = SliderImage.objects.filter(is_visible=True,slider_number=slider_number)
    
    if randomize:
        qs = qs.order_by('?')

    if limit:
        qs = qs[0:limit]
    
    return qs
