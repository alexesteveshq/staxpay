from odoo import models, fields

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('staxpay', 'StaxPay')], ondelete={'staxpay': 'set default'})
    staxpay_public_key = fields.Char(string='StaxPay Public Key')
