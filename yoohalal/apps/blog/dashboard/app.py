from django.conf.urls import url

from oscar.core.application import DashboardApplication
from oscar.core.loading import get_class


class BlogDashboardConfig(DashboardApplication):
    name = None
    default_permissions = ['is_staff', ]

    list_view   = get_class('apps.blog.dashboard.views', 'PostListView')
    create_view = get_class('apps.blog.dashboard.views', 'PostCreateView')
    update_view = get_class('apps.blog.dashboard.views', 'PostUpdateView')
    delete_view = get_class('apps.blog.dashboard.views', 'PostDeleteView')
    detail_view = get_class('apps.blog.dashboard.views', 'PostDetailView')

    c_list_view   = get_class('apps.blog.dashboard.views', 'CategoryListView')
    c_create_view = get_class('apps.blog.dashboard.views', 'CategoryCreateView')
    c_update_view = get_class('apps.blog.dashboard.views', 'CategoryUpdateView')
    c_delete_view = get_class('apps.blog.dashboard.views', 'CategoryDeleteView')
    c_detail_view = get_class('apps.blog.dashboard.views', 'CategoryDetailView')

    def get_urls(self):
        urls = [
            # Post
            url(r'^$', self.list_view.as_view(), name='post-list'),
            url(r'^create/$', self.create_view.as_view(), name='post-create'),
            url(r'^delete/(?P<pk>\d+)/$', self.delete_view.as_view(), name='post-delete'),
            url(r'^update/(?P<pk>\d+)/$', self.update_view.as_view(), name='post-update'),
            url(r'^view/(?P<pk>\d+)/$', self.detail_view.as_view(), name='post-detail'),
            # Category
            url(r'^categories/$', self.c_list_view.as_view(), name='category-list'),
            url(r'^create-category/$', self.c_create_view.as_view(), name='category-create'),
            url(r'^delete-category/(?P<pk>\d+)/$', self.c_delete_view.as_view(), name='category-delete'),
            url(r'^update-category/(?P<pk>\d+)/$', self.c_update_view.as_view(), name='category-update'),
            url(r'^view-category/(?P<pk>\d+)/$', self.c_detail_view.as_view(), name='category-detail'),
        ]
        return self.post_process_urls(urls)


application = BlogDashboardConfig()
