from django.conf.urls import url

from oscar.core.application import DashboardApplication
from oscar.core.loading import get_class


class ConfirmationDashboardApplication(DashboardApplication):
    name = None
    default_permissions = ['is_staff', ]

    list_view   = get_class('confirmation.dashboard.views', 'ConfirmationListView')
    detail_view = get_class('confirmation.dashboard.views', 'ConfirmationDetailView')
    change_status_view = get_class('confirmation.dashboard.views', 'ConfirmationChangeStatusView')

    def get_urls(self):
        urls = [
            url(r'^$', self.list_view.as_view(), name='confirmation-method-list'),
            url(r'^view/(?P<pk>\d+)/$', self.detail_view.as_view(), name='confirmation-method-detail'),
            url(r'^change/(?P<pk>\d+)/'
                r'(?P<action>(accept|reject))/$',
                self.change_status_view.as_view(),
                name='confirmation-change-status'),
        ]

        return self.post_process_urls(urls)


application = ConfirmationDashboardApplication()
