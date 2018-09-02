from django.conf.urls import url

from oscar.core.application import DashboardApplication
from oscar.core.loading import get_class


class CareerDashboardApplication(DashboardApplication):
    name = None
    default_permissions = ['is_staff', ]

    list_view   = get_class('apps.career.dashboard.views', 'CareerListView')
    create_view = get_class('apps.career.dashboard.views', 'CareerCreateView')
    update_view = get_class('apps.career.dashboard.views', 'CareerUpdateView')
    delete_view = get_class('apps.career.dashboard.views', 'CareerDeleteView')
    detail_view = get_class('apps.career.dashboard.views', 'CareerDetailView')

    applicant_list_view   = get_class('apps.career.dashboard.views', 'ApplicantListView')
    applicant_detail_view = get_class('apps.career.dashboard.views', 'ApplicantDetailView')
    applicant_delete_view = get_class('apps.career.dashboard.views', 'ApplicantDeleteView')

    departement_list_view   = get_class('apps.career.dashboard.views', 'DepartementListView')
    departement_create_view = get_class('apps.career.dashboard.views', 'DepartementCreateView')
    departement_update_view = get_class('apps.career.dashboard.views', 'DepartementUpdateView')
    departement_delete_view = get_class('apps.career.dashboard.views', 'DepartementDeleteView')
    departement_detail_view = get_class('apps.career.dashboard.views', 'DepartementDetailView')

    def get_urls(self):
        urls = [
            url(r'^applicants$', self.applicant_list_view.as_view(), name='applicant-list'),
            url(r'^view-applicant/(?P<pk>\d+)/$', self.applicant_detail_view.as_view(), name='applicant-detail'),
            url(r'^delete-applicant/(?P<pk>\d+)/$', self.applicant_delete_view.as_view(), name='applicant-delete'),

            # Career
            url(r'^list/$', self.list_view.as_view(), name='career-list'),
            url(r'^create/$', self.create_view.as_view(), name='career-create'),
            url(r'^delete/(?P<pk>\d+)/$', self.delete_view.as_view(), name='career-delete'),
            url(r'^update/(?P<pk>\d+)/$', self.update_view.as_view(), name='career-update'),
            url(r'^view/(?P<pk>\d+)/$', self.detail_view.as_view(), name='career-detail'),

            # Departement
            url(r'^departements/$', self.departement_list_view.as_view(), name='departement-list'),
            url(r'^create-departement/$', self.departement_create_view.as_view(), name='departement-create'),
            url(r'^delete-departement/(?P<pk>\d+)/$', self.departement_delete_view.as_view(), name='departement-delete'),
            url(r'^update-departement/(?P<pk>\d+)/$', self.departement_update_view.as_view(), name='departement-update'),
            url(r'^view-departement/(?P<pk>\d+)/$', self.departement_detail_view.as_view(), name='departement-detail'),

        ]

        return self.post_process_urls(urls)


application = CareerDashboardApplication()
