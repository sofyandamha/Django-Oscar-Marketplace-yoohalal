from django.conf.urls import url

from oscar.apps.customer.app import CustomerApplication as CoreCustomerApplication
from oscar.core.loading import get_class

class CustomerApplication(CoreCustomerApplication):
    activate_view = get_class('apps.customer.views', 'ActivateView')
    after_view = get_class('apps.customer.views', 'AfterRegisterView')

    def get_urls(self):
        urls = super(CustomerApplication, self).get_urls()
        urls += [
            url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                self.activate_view.as_view(), name='activate'),
            url(r'^after-register/(?P<uidb64>[0-9A-Za-z_\-]+)/$', self.after_view.as_view(),
                name='after-register')
        ]
        
        return self.post_process_urls(urls)

application = CustomerApplication()