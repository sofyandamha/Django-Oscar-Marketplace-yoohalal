from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SliderDashboardConfig(AppConfig):
    label = 'slider_dashboard'
    name = 'slider.dashboard'
    verbose_name = _('Slider Dashboard')