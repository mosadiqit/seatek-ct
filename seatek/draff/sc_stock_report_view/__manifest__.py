# -*- coding: utf-8 -*-
{
    'name': "Seacorp Inventory report view",

    'summary': """
        Seacorp Inventory report view
        """,

    'description': """
        Seacorp Inventory report view
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'stock',
    'version': '12.0.0.1.00002',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'product', 'mrp'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
        'views/sc_stock_quantity_history.xml',
        'views/sc_view_stock_product_tree.xml',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': False,
    'auto_install': False,
}