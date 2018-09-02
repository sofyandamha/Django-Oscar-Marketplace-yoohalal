import random
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, render,redirect

from .models import PostEntry, Category
from meta.views import MetadataMixin

class BlogListView(ListView):
	model = PostEntry
	context_object_name = 'posts'
	template_name = 'blog/blog_index.html'
	queryset = PostEntry.objects.published().all()
	paginate_by = 10

	def get_context_data(self, **kwargs):
		context = super(BlogListView, self).get_context_data(**kwargs)
		context['categories_list'] = Category.objects.order_by('category')
		context['title'] = _('Blog')
		return context

class CategoryListView(ListView):
	model = Category
	context_object_name = 'posts'
	template_name = 'blog/blog_category.html'
	paginate_by = 10

	def get_queryset(self):
		self.category = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
		queryset = PostEntry.objects.published().filter(category=self.category)
		return queryset

	def get_context_data(self, **kwargs):
		context = super(CategoryListView, self).get_context_data(**kwargs)
		context['categories_list'] = Category.objects.order_by('category')		
		context['title'] = self.category.category
		return context

class BlogDetailView(DetailView):
	model = PostEntry
	template_name = 'blog/blog_detail.html'
	context_object_name = 'post'

	def get(self, request, *args, **kwargs):
		try:
			self.object = self.get_object()
		except Http404:
			return redirect('blog:blog-list')
		context = self.get_context_data(object=self.object)
		return self.render_to_response(context)

	def get_object(self):
		post = get_object_or_404(PostEntry,slug=self.kwargs['slug'])
		return post

	def get_context_data(self, **kwargs):
		context = super(BlogDetailView, self).get_context_data(**kwargs)
		post = self.get_object()
		context['categories_list'] = Category.objects.order_by('category')
		context['meta'] = self.get_object().as_meta()
		context["title"] = post.title
		
		return context