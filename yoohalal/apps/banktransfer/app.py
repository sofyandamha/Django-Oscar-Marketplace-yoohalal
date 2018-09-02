from django.apps import AppConfig
from oscar.apps.checkout.app import CheckoutApplication
from django.conf.urls import url
from . import views

class BanktransferConfig(AppConfig):
	name = 'banktransfer'

class OverriddenCheckoutApplication(CheckoutApplication):
	payment_details_view = views.PaymentDetailsView

application = OverriddenCheckoutApplication()
