from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ConfirmationDashboardConfig(AppConfig):
    label = 'confirmation_dashboard'
    name = 'confirmation.dashboard'
    verbose_name = _('Confirmation Dashboard')