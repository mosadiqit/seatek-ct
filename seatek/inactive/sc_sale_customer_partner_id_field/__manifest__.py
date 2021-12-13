# -*- coding: utf-8 -*-
{
    'name': "Seacorp Sale Customer Partner Field ( Obsoleted) ",

    'summary': """
        Seacorp Sale Customer Partner Field""",

    'description': """
       Seacorp Sale Customer Partner Field -> Merge to sea_sale_order_extend
       Old : 
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sale',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',

        'views/sale_order_view.xml',
    ],
    # only loaded in demonstration mode
}