# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, _
from odoo.exceptions import ValidationError

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'staxpay':
            return res

        return {
            'api_url': '/payment/staxpay/process',
            'reference': self.reference,
        }

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'staxpay' or len(tx) == 1:
            return tx

        reference = notification_data.get('reference')
        tx = self.search([('reference', '=', reference), ('provider_code', '=', 'staxpay')])
        if not tx:
            raise ValidationError(
                "Staxpay: " + _("No transaction found matching reference %s.", reference)
            )
        return tx

    def _process_notification_data(self, notification_data):
        super()._process_notification_data(notification_data)
        if self.provider_code != 'staxpay':
            return

        self.payment_method_id = self.env['payment.method']._get_from_code('staxpay')

        response_code = notification_data.get('status')
        if response_code == '200':
            self._set_done()
        else:
            self._set_error(_("Unrecognized response received from the payment provider."))
