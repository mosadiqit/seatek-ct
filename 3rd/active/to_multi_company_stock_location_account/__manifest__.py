{
    'name': "Multi Company Stock Location Account",

    'summary': """
Add multi-company support for stock location accounts
        """,

    'description': """
The problem
===========
In Odoo, with Inventory Valuation enabled, when you transfer goods in/out locations (e.g. Inventory adjustment, Production)
that have Stock Valuation Accounts specified, Odoo will also generate accounting journal entries automatically based on those stock valuation accounts.

However, these Stock Valuation Accounts fields of the stock location model do not respect multi-company enviroment.
In other words, every inventory adjustment move will be encoded into the same company's accounts no matter the company of the adjustment is.

The solution
============

This module fixes the above problem by supporting multi-company environment for stock location's valuation accounts.
With this module, every inventory adjustment / manufaturing moves now respect the company of the operation
    """,

    'author': 'T.V.T Marine Automation (aka TVTMA),Viindoo',
    'website': 'https://viindoo.com',
    'live_test_url': 'https://v12demo-int.erponline.vn',
    'support': 'apps.support@viindoo.com',

    'category': 'Warehouse',
    'version': '1.0.0',

    'depends': ['stock_account'],

    'data': [       
        'views/stock_location_view.xml',
        'data/stock_location_data.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
    'price': 45.9,
    'currency': 'EUR',
    'license': 'OPL-1',
}
