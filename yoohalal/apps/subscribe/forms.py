from django import forms

from oscar.core.loading import get_class, get_model

from .models import SubscribeBase


CommunicationEventType = get_model('customer', 'CommunicationEventType')
Dispatcher = get_class('customer.utils', 'Dispatcher')

class SubscribeForm(forms.ModelForm):

	def send_email(self, site, recipient, ref):
		code = 'SUBSCRIBE'
		unsubscribe_url = "https://{0}/newsletter/unsubscribe/{1}".format(site, ref)
		ctx = {'site': site, 'unsubscribe_url' : unsubscribe_url}
		try:
			event_type = CommunicationEventType.objects.get(code=code)
		except CommunicationEventType.DoesNotExist:
			messages = CommunicationEventType.objects.get_and_render(code, ctx)
		else:
			messages = event_type.get_messages(ctx)

		if messages and messages['body']:
			Dispatcher().dispatch_direct_messages(recipient, messages)

	class Meta:
		model = SubscribeBase
		fields = ('email',)