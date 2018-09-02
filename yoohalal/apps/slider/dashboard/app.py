from django.conf.urls import url

from oscar.core.application import DashboardApplication
from oscar.core.loading import get_class


class SliderDashboardConfig(DashboardApplication):
    name = None
    default_permissions = ['is_staff', ]

    list_view   = get_class('apps.slider.dashboard.views', 'SliderListView')
    create_view = get_class('apps.slider.dashboard.views', 'SliderCreateView')
    update_view = get_class('apps.slider.dashboard.views', 'SliderUpdateView')
    delete_view = get_class('apps.slider.dashboard.views', 'SliderDeleteView')
    detail_view = get_class('apps.slider.dashboard.views', 'SliderDetailView')

    def get_urls(self):
        urls = [
            url(r'^$', self.list_view.as_view(), name='slider-list'),
            url(r'^create/$', self.create_view.as_view(), name='slider-create'),
            url(r'^delete/(?P<pk>\d+)/$', self.delete_view.as_view(), name='slider-delete'),
            url(r'^update/(?P<pk>\d+)/$', self.update_view.as_view(), name='slider-update'),
            url(r'^view/(?P<pk>\d+)/$', self.detail_view.as_view(), name='slider-detail'),
        ]

        return self.post_process_urls(urls)


application = SliderDashboardConfig()
