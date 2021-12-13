# -*- coding: utf-8 -*-
{
    'name': "Seacorp Inventory Adjustment report XLS",

    'summary': """
       Seacorp Inventory Adjustment report XLS""",

    'description': """
        Seacorp Inventory Adjustment report XLS
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

    'category': 'stock',
    'version': '10.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],

    # always loaded
    'data': [

        'reports/inventory_adjustment_report.xml',
    ],
}