from django.utils.translation import ugettext_lazy as _
from oscar.apps.payment.forms import *

class BillingAddressForm(BillingAddressForm):

	class Meta(BillingAddressForm.Meta):
		fields = ['full_name', 'full_address', 'sub_districts', 'city'] + BillingAddressForm.Meta.fields

	def __init__(self, *args, **kwargs):
		super(BillingAddressForm, self).__init__(*args, **kwargs)
		for field in ['title', 'first_name', 'last_name', 'line1', 'line2', 'line3', 'line4']:
			self.fields.pop(field)
		self.fields['phone_number'].label = _('Phone number')
		self.fields['full_address'].widget.attrs['rows'] = 3