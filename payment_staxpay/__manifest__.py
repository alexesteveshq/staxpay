# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'StaxPay Payment Integration',
    'summary': 'Allow payments with Staxpay on website. (staxpay | stax payment | stax)',
    'description': 'Allow payments with Staxpay on website',
    'version': '17.0.1.0',
    'category': 'Accounting/Website',
    'author': 'Visionee',
    'license': 'OPL-1',
    'depends': ['payment', 'partner_firstname'],
    'assets': {
        'web.assets_frontend': [
            'payment_staxpay/static/src/js/payment_form.js',
            'payment_staxpay/static/src/css/payment_staxpay.css',
        ],
    },
    'data': [
        'views/payment_form_templates.xml',
        'views/payment_provider_views.xml',
        'data/payment_provider_data.xml',
    ],
    'images': [
        'static/description/banner.png',
    ],
    'price': 100,
    'currency': "EUR",
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
}