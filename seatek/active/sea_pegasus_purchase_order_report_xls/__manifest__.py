# -*- coding: utf-8 -*-
{
    'name': "Sea Pegasus Purchase Report - XLS",

    'summary': """
       Pegasus Purchase Order XLS""",

    'description': """
        Pegasus Purchase Order XLS
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

    'category': 'purchase',
    'version': '10.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase'],

    # always loaded
    'data': [

        'reports/purchase_order_report.xml',
    ],
}