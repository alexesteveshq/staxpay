import logging

from odoo import http
from odoo.http import request, route

_logger = logging.getLogger(__name__)

class StaxPaymentController(http.Controller):

    @route('/payment/staxpay/process', type='http', auth='public', methods=['POST'], csrf=False, cors='*')
    def staxpay_process_transaction(self, **post):
        request.env['payment.transaction'].sudo()._handle_notification_data(
            'staxpay', {'reference': post.get('reference'), 'status': '200'})
        return request.redirect('/payment/status')

    @route('/payment/staxpay/get_data', type='json', auth='public', csrf=False, cors='*')
    def staxpay_process_data(self, **kwargs):
        customer = request.env['res.partner'].sudo().search([('id', '=', kwargs.get('partner_id'))])
        merchant_code = request.env['ir.config_parameter'].sudo().get_param('database.uuid')
        data = {'merchant_code': merchant_code}
        if customer:
            if customer.phone and len(customer.phone) < 10:
                return {'error': 'Phone number must be at least 10 numbers and include area code.'
                                 ' Please configure the phone in your account to match the format'}
            firstname = customer.name.split(" ")[0]
            lastname = customer.name.split(" ")[-1]
            data.update({
                'firstname': firstname,
                'lastname': lastname,
                'phone': customer.phone,
                'address': customer.contact_address_complete,
                'city': customer.city,
                'state': customer.state_id.name,
                'zip': customer.zip,
                'country': customer.country_id.name,
            })
        return data
