from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SocialMediaDashboardConfig(AppConfig):
    label = 'social_dashboard'
    name = 'social_media.dashboard'
    verbose_name = _('Social Media Dashboard')