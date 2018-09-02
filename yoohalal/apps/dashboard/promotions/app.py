from django.conf.urls import url

from oscar.apps.dashboard.promotions.app import PromotionsDashboardApplication as CorePromotionsDashboardApplication
from oscar.core.loading import get_class

from apps.promotions.conf import PROMOTION_CLASSES


class PromotionsDashboardApplication(CorePromotionsDashboardApplication):

	# Dynamically set the CRUD views for all promotion classes
	view_names = (
		('create_%s_view', 'Create%sView'),
		('update_%s_view', 'Update%sView'),
		('delete_%s_view', 'Delete%sView')
	)
	for klass in PROMOTION_CLASSES:
		if klass.classname() == 'categoryproductlist':
			for attr_name, view_name in view_names:
				full_attr_name = attr_name % klass.classname()
				full_view_name = view_name % klass.__name__
				view = get_class('apps.dashboard.promotions.views', full_view_name)
				locals()[full_attr_name] = view

	def get_urls(self):
		urls = super(PromotionsDashboardApplication, self).get_urls()

		for klass in PROMOTION_CLASSES:
			if klass.classname() == 'categoryproductlist':
				code = klass.classname()
				urls += [
					url(r'create/%s/' % code,
						getattr(self, 'create_%s_view' % code).as_view(),
						name='promotion-create-%s' % code),
					url(r'^update/(?P<ptype>%s)/(?P<pk>\d+)/$' % code,
						getattr(self, 'update_%s_view' % code).as_view(),
						name='promotion-update'),
					url(r'^delete/(?P<ptype>%s)/(?P<pk>\d+)/$' % code,
						getattr(self, 'delete_%s_view' % code).as_view(),
						name='promotion-delete')]

		return self.post_process_urls(urls)


application = PromotionsDashboardApplication()
