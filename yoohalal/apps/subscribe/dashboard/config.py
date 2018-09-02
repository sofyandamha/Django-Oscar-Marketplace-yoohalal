from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SubscribeDashboardConfig(AppConfig):
    label = 'subscribe_dashboard'
    name = 'subscribe.dashboard'
    verbose_name = _('Subscribe Dashboard')