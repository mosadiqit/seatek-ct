# -*- coding: utf-8 -*-
{
    'name': "Seacorp Purchase Payment Request",

    'summary': """
        Print Payment Request""",

    'description': """
        Seacorp Purchase -> Print Payment Request
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'purchase',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/payment_request_templates.xml',
        'views/payment_request_view.xml',
    ],
}