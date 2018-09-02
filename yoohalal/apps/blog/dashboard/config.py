from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class BlogDashboardConfig(AppConfig):
    label = 'blog_dashboard'
    name = 'blog.dashboard'
    verbose_name = _('Blog Dashboard')

class CategoryDashboardConfig(AppConfig):
    label = 'category_dashboard'
    name = 'Category.dashboard'
    verbose_name = _('Category Dashboard')