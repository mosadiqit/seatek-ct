# -*- coding: utf-8 -*-
{
    'name': "Seacorp add Delivery field to Sale order line",

    'summary': """
        Seacorp add Delivery field to Sale order line""",

    'description': """
        Seacorp add Delivery field to Sale order line
    """,

    'author': "Seatek",
    'website': "https://seacorp.vn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order_view.xml'
    ],
}