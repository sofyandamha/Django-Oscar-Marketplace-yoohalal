from django.views.generic import (
	CreateView, DeleteView, ListView, UpdateView, View, DetailView)
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy
from apps.blog.models import PostEntry, Category
from apps.blog.forms import PostForm, CategoryForm
from apps.blog.dashboard.tables import CategoryTable, PostTable
from apps.blog.dashboard.forms import CategorySearchForm, PostSearchForm

from django_tables2 import SingleTableView


# ============
# CREATE VIEWS
# ============

class PostCreateView(CreateView):
	model = PostEntry
	form_class = PostForm
	template_name = 'dashboard/post/post_form.html'
	success_url =  reverse_lazy('post-list')

	def get_success_url(self):
		messages.info(self.request, _("Post created successfully"))
		return super(PostCreateView, self).get_success_url()

	def get_context_data(self, **kwargs):
		ctx = super(PostCreateView, self).get_context_data(**kwargs)
		ctx['title'] = _("Create Post")
		return ctx


class CategoryCreateView(CreateView):
	model = Category
	form_class = CategoryForm
	template_name = 'dashboard/category/category_form.html'
	success_url =  reverse_lazy('category-list')

	def get_success_url(self):
		messages.info(self.request, _("Category created successfully"))
		return super(CategoryCreateView, self).get_success_url()

	def get_context_data(self, **kwargs):
		ctx = super(CategoryCreateView, self).get_context_data(**kwargs)
		ctx['title'] = _("Create Category")
		return ctx

# ============
# UPDATE VIEWS
# ============

class PostUpdateView(UpdateView):
	model = PostEntry
	form_class = PostForm
	template_name = 'dashboard/post/post_form.html'
	success_url = reverse_lazy('post-list')

	def get_success_url(self):
		messages.info(self.request, _("Post updated successfully"))
		return super(PostUpdateView, self).get_success_url()

	def get_context_data(self, **kwargs):
		ctx = super(PostUpdateView, self).get_context_data(**kwargs)
		ctx['post'] = self.object
		ctx['title'] = self.object.title
		return ctx


class CategoryUpdateView(UpdateView):
	model = Category
	form_class = CategoryForm
	template_name = 'dashboard/category/category_form.html'
	success_url =  reverse_lazy('category-list')

	def get_success_url(self):
		messages.info(self.request, _("Category updated successfully"))
		return super(CategoryUpdateView, self).get_success_url()

	def get_context_data(self, **kwargs):
		ctx = super(CategoryUpdateView, self).get_context_data(**kwargs)
		ctx['category'] = self.object
		ctx['title'] = self.object.category
		return ctx

# ============
# DELETE VIEWS
# ============

class PostDeleteView(DeleteView):
	model = PostEntry
	context_object_name = 'post'
	template_name = 'dashboard/post/post_delete.html'
	success_url =  reverse_lazy('post-list')

	def get_success_url(self):
		messages.info(self.request, _("Post deleted"))
		return reverse('post-list')


class CategoryDeleteView(DeleteView):
	model = Category
	context_object_name = 'category'
	template_name = 'dashboard/category/category_delete.html'
	success_url =  reverse_lazy('category-list')

	def get_success_url(self):
		messages.info(self.request, _("Category deleted"))
		return reverse('category-list')

# ============
# LIST VIEWS
# ============

class PostListView(SingleTableView):
	model = PostEntry
	table_class = PostTable
	form_class = PostSearchForm
	context_table_name = 'posts'
	template_name = 'dashboard/post/post_list.html'

	def get_context_data(self, **kwargs):
		ctx = super(PostListView, self).get_context_data(**kwargs)
		ctx['form'] = self.form
		return ctx

	def get_description(self, form):
		if form.is_valid() and any(form.cleaned_data.values()):
			return _('Posts search results')
		return _('Posts')

	def get_table(self, **kwargs):
		table = super(PostListView, self).get_table(**kwargs)
		table.caption = self.get_description(self.form)
		return table

	def get_table_pagination(self, table):
		return dict(per_page=20)

	def get_queryset(self):
		queryset = self.model.objects.all()
		self.form = self.form_class(self.request.GET)
		if not self.form.is_valid():
			return queryset
		data = self.form.cleaned_data
		if data['title']:
			queryset = queryset.filter(title__icontains=data['title'])
		return queryset


class CategoryListView(SingleTableView):
	model = Category
	table_class = CategoryTable
	form_class = CategorySearchForm
	context_table_name = 'categories'
	template_name = 'dashboard/category/category_list.html'

	def get_context_data(self, **kwargs):
		ctx = super(CategoryListView, self).get_context_data(**kwargs)
		ctx['form'] = self.form
		return ctx

	def get_description(self, form):
		if form.is_valid() and any(form.cleaned_data.values()):
			return _('Categories search results')
		return _('Categories')

	def get_table(self, **kwargs):
		table = super(CategoryListView, self).get_table(**kwargs)
		table.caption = self.get_description(self.form)
		return table

	def get_table_pagination(self, table):
		return dict(per_page=20)

	def get_queryset(self):
		queryset = self.model.objects.all()
		self.form = self.form_class(self.request.GET)
		if not self.form.is_valid():
			return queryset
		data = self.form.cleaned_data
		if data['category']:
			queryset = queryset.filter(category__icontains=data['category'])
		return queryset

# ============
# DETAIL VIEWS
# ============

class PostDetailView(DetailView):
	model = PostEntry
	context_object_name = 'txn'
	template_name = 'dashboard/post/post_detail.html'


class CategoryDetailView(DetailView):
	model = Category
	context_object_name = 'txn'
	template_name = 'dashboard/category/category_detail.html'