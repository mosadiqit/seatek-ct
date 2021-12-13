# -*- coding: utf-8 -*-
{
    'name': "Sea Sale Order Extend",

    'summary': """
        Extend Sale Order""",
    'category': 'sale',
    'version': '12.0.0.3',

    'description': """
       Extend Sale Order
       12.0.0.3 : Add ship Contact Type
    """,

    'author': "Seatek",
    'website': "https://home.seacorp.vn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list


    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order_view.xml',
    ],
    # only loaded in demonstration mode
}