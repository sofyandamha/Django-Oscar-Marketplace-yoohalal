from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CareerDashboardConfig(AppConfig):
    label = 'career_dashboard'
    name = 'career.dashboard'
    verbose_name = _('Career Dashboard')