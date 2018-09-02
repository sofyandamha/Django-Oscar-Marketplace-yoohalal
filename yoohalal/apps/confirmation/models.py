import os

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.validators import FileExtensionValidator


class ConfirmationPayment(models.Model):
    order_number = models.CharField(_('Order Number'), max_length=128)
    transfer_date = models.DateTimeField(_('Transfer Date'), default=timezone.now)    
    destination_bank = models.CharField(_('Destination Bank'), max_length=250)
    amount = models.DecimalField(_('Amount'), max_digits=12, decimal_places=2, null=False, blank=False)
    account_owner_name = models.CharField(_('Account Owner Name'), max_length=250)
    customer_email = models.EmailField(_('Customer Email'))
    customer_phone = models.CharField(_('Customer Phone'), max_length=250,
        blank=True, help_text=_("In case we need to call you about your order"))
    note = models.TextField(_('Note'))
    proof_payment = models.FileField(
                            _('Proof Of Payment'),
                            null=True,
                            upload_to=settings.CONFIRMATION_IMAGE_FOLDER,
                            validators=[FileExtensionValidator(['pdf','doc','docx','jpg','jpeg','png'])]
                        )

    date_created = models.DateTimeField(_('Date Created'), auto_now_add=True)
    status = models.CharField(
                        _("Status"), max_length=50,
                        choices=settings.CONFIRMATION_STATUS, default='pending'
                    )

    class Meta:
        ordering = ('-date_created',)
        app_label = 'confirmation'
        verbose_name = _('Confirmation Payment')

    @property
    def filename(self):
        return os.path.basename(self.proof_payment.name)

    @property
    def _as_table(self, params):
        rows = []
        for k, v in sorted(params.items()):
            rows.append('<tr><th>%s</th><td>%s</td></tr>' % (k, v[0]))
        return '<table>%s</table>' % ''.join(rows)