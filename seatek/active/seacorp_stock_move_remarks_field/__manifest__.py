# -*- coding: utf-8 -*-
{
    'name': "Seacorp Stock move remarks field",

    'summary': """
        Seacorp Stock move remarks field""",

    'description': """
        Seacorp Stock move remarks field
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'stock',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'sale_stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_view.xml'
    ],
    'css': [
        'static/src/css/font.css',
    ],
    # only loaded in demonstration mode
}