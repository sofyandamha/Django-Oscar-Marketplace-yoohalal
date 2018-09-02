from django.conf.urls import url

from oscar.core.application import DashboardApplication
from oscar.core.loading import get_class


class BankTransferDashboardApplication(DashboardApplication):
    name = None
    default_permissions = ['is_staff', ]

    list_view   = get_class('apps.banktransfer.dashboard.views', 'TransactionListView')
    detail_view = get_class('apps.banktransfer.dashboard.views', 'TransactionDetailView')

    def get_urls(self):
        urls = [
            url(r'^$', self.list_view.as_view(), name='banktransfer-transaction-list'),
            url(r'^view/(?P<pk>\d+)/$', self.detail_view.as_view(), name='banktransfer-transaction-detail'),
        ]

        return self.post_process_urls(urls)


application = BankTransferDashboardApplication()