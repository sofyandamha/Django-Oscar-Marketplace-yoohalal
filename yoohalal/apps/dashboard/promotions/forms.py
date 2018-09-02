from django import forms
from django.utils.translation import ugettext_lazy as _

from apps.promotions.conf import PROMOTION_CLASSES


class PromotionTypeSelectForm(forms.Form):
	choices = []
	for klass in PROMOTION_CLASSES:
		choices.append((klass.classname(), klass._meta.verbose_name))
	promotion_type = forms.ChoiceField(choices=tuple(choices),
									   label=_("Promotion type"))