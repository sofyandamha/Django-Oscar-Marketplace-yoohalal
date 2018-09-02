from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class BanktransferDashboardConfig(AppConfig):
    label = 'banktransfer_dashboard'
    name = 'banktransfer.dashboard'
    verbose_name = _('Bank Transfer Dashboard')