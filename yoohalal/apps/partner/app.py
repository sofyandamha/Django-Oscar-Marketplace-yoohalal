import django
from django.conf.urls import url
from oscar.core.application import Application
from . import views

class PartnerApplication(Application):
    name = 'partner'

    registration_view = views.PartnerRegistrationView
    success_view = views.RegistrationSuccessView

    def get_urls(self):
        urlpatterns = [
            url(r'^partner-registration/$', self.registration_view.as_view(), 
                name='partner-registration'),
            url(r'^registration-success/(?P<partner_id>[-\w]+)/$', self.success_view.as_view(), 
                name='registration-success'),
        ]
        
        return self.post_process_urls(urlpatterns)


application = PartnerApplication()
