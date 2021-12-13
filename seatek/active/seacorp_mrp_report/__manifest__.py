# -*- coding: utf-8 -*-
{
    'name': "Seacorp Manufacturing Report",

    'summary': """
        Seacorp Manufacturing Report View""",

    'description': """
        Seacorp Manufacturing Report View
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'mrp',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp'],

    # always loaded
    'data': [
        'views/views.xml',

    ],
    
}