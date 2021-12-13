# -*- coding: utf-8 -*-
{
    'name': "Seacorp Pos Retail Repord pdf",

    'summary': """
       Seacorp Pos Retail Repord pdf""",

    'description': """
        Seacorp Pos Retail Repord pdf
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Point of Sale',
    'version': '8.0.1.6',

    # any module necessary for this one to work correctly
    'depends': ['base', 'pos_retail'],

    # always loaded
    'data': [
        'views/pos_sale_report_view.xml',
        'reports/seacorp_pos_sale_report_template.xml',
    ],
}