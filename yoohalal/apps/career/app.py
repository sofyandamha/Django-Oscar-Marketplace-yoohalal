import django
from django.conf.urls import url
from oscar.core.application import Application
from oscar.core.loading import get_class


class CareerApplication(Application):
	name = 'career'

	career_list = get_class('apps.career.views', 'CareerListView')
	career_detail = get_class('apps.career.views', 'CareerDetailView')
	applicant_form = get_class('apps.career.views', 'ApplicantView')
	applicant_thanks = get_class('apps.career.views', 'ThanksView')

	def get_urls(self):
		urlpatterns = [

			url(r'^$', self.career_list.as_view(), name='career-list'),
			url(r'^applicant-form/(?P<career_id>[-\w]+)/$', self.applicant_form.as_view(), name='applicant-form'),
			url(r'^applicant-thanks/(?P<career_id>[-\w]+)/(?P<ref>[-\w]+)/$', self.applicant_thanks.as_view(), name='applicant-thanks'),
			url(r'^(?P<slug>[-\w]+)/$', self.career_detail.as_view(), name='career-detail'),
		]

		return self.post_process_urls(urlpatterns)

application = CareerApplication()
