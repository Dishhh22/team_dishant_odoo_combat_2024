{
    'name': 'Furniture Rental',
    'version': '16.0',
    'category': 'Sales',
    'author': "Team Dishant",
    'maintainer': "Team Dishant",
    'summary': 'Manage furniture rentals',
    'description': """
        This module allows you to manage furniture rentals, including:
        - Furniture item management
        - Booking and reservations
        - Customer profiles
    """,
    'depends': ['base', 'product', 'sale', 'website_sale', 'sale_renting', 'payment_paystack', 'stock'],
    'data': [
        'data/product_category_data.xml',
        'data/product_template_data.xml',
        'views/templates.xml',
    ],
    'demo': [],
    'assets': {
        'web.assets_frontend': [
            'furniture_renting_system/static/src/css/*',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
