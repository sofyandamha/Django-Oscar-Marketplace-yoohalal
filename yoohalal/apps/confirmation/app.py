from django.conf.urls import url
from django.views.generic.base import TemplateView

from oscar.core.application import Application
from oscar.core.loading import get_class

class ConfirmationApplication(Application):
    name = 'confirmation'

    order_view   = get_class('apps.confirmation.views', 'ConfirmationOrderView')
    confirm_view   = get_class('apps.confirmation.views', 'ConfirmationPaymentView')
    success_view = get_class('apps.confirmation.views', 'ConfirmationSuccessView')

    def get_urls(self):
        urls = [
            url(r'^pembayaran', TemplateView.as_view(template_name='confirmation/payment.html'), name="payment-page"),
            url(r'^confirm-order/$', self.order_view.as_view(), name='confirmation-order'),
            url(r'^confirm-payment/(?P<order_number>[-\w]+)/$', self.confirm_view.as_view(), name='confirmation-payment'),
            url(r'^confirm-success/(?P<order_number>[-\w]+)/$', self.success_view.as_view(), name='confirmation-success'),
        ]
        
        return self.post_process_urls(urls)


application = ConfirmationApplication()
