{
    'name': 'Paystack Payment Acquirer',
    'category': 'Accounting/Payment Acquirers',
    'summary': 'Payment Acquirer: Paystack Implementation',
    "version": "16.0.1.0.2",
    'description': """Paystack Payment Acquirer""",
    'author': 'Team Dishant',
    'depends': ['payment', 'website_sale'],
    'data': [
        'views/paystack_view.xml',
        'views/payment_acquirer.xml',
        'data/paystack_data.xml',
        'views/payment_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'payment_paystack/static/src/js/*.*',
        ],
    },
    'installable': True,
    'uninstall_hook': 'uninstall_hook',
    'price': 110,
    'currency': 'USD',
    'license': 'OPL-1',
    'images': ['static/description/image.png'],
}
