from django.conf.urls import url

from oscar.core.application import DashboardApplication
from oscar.core.loading import get_class


class SubscribeDashboardApplication(DashboardApplication):
    name = None
    default_permissions = ['is_staff', ]

    list_view   = get_class('apps.subscribe.dashboard.views', 'SubscribeListView')
    detail_view = get_class('apps.subscribe.dashboard.views', 'SubscribeDetailView')

    def get_urls(self):
        urls = [
            url(r'^$', self.list_view.as_view(), name='subscribe-list'),
            url(r'^view/(?P<pk>\d+)/$', self.detail_view.as_view(), name='subscribe-detail'),
        ]

        return self.post_process_urls(urls)


application = SubscribeDashboardApplication()
