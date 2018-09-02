from django.conf.urls import url

from oscar.core.application import DashboardApplication
from oscar.core.loading import get_class


class SocialMediaDashboardConfig(DashboardApplication):
    name = None
    default_permissions = ['is_staff', ]

    list_view   = get_class('apps.social_media.dashboard.views', 'LinkTypeListView')
    create_view = get_class('apps.social_media.dashboard.views', 'LinkTyCreateView')
    update_view = get_class('apps.social_media.dashboard.views', 'LinkTypeUpdateView')
    delete_view = get_class('apps.social_media.dashboard.views', 'LinkTypeDeleteView')
    detail_view = get_class('apps.social_media.dashboard.views', 'LinkTypeDetailView')


    def get_urls(self):
        urls = [
            url(r'^$', self.list_view.as_view(), name='link-list'),
            url(r'^create/$', self.create_view.as_view(), name='link-create'),
            url(r'^update/(?P<pk>\d+)/$', self.update_view.as_view(), name='link-update'),
            url(r'^delete/(?P<pk>\d+)/$', self.delete_view.as_view(), name='link-delete'),
            url(r'^detail/(?P<pk>\d+)/$', self.detail_view.as_view(), name='link-detail'),
        ]

        return self.post_process_urls(urls)


application = SocialMediaDashboardConfig()
