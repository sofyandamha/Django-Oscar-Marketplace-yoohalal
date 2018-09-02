import django

from django.conf.urls import url
from oscar.core.application import Application
from oscar.core.loading import get_class

class BlogApplication(Application):
	name = 'blog'

	blog_list = get_class('apps.blog.views', 'BlogListView')
	blog_detail = get_class('apps.blog.views', 'BlogDetailView')
	category_list = get_class('apps.blog.views', 'CategoryListView')

	def get_urls(self):
		urls = [
			url(r'^$', self.blog_list.as_view(), name='blog-list'),
			url(r'^(?P<slug>[-\w]+)/$', self.blog_detail.as_view(), name='blog-detail'),
			url(r'^category/(?P<cat_slug>[-\w]+)/$', self.category_list.as_view(), name='category-list')
		]
		
		return self.post_process_urls(urls)

application = BlogApplication()
