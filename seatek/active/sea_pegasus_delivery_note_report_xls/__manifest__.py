# -*- coding: utf-8 -*-
{
    'name': "Sea Pegasus Delivery Note - XLS",

    'summary': """
       Pegasus Delivery Note XLS""",

    'description': """
      Pegasus Delivery Note XLS
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

    'category': 'stock',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],

    # always loaded
    'data': [

        'reports/delivery_note_report.xml',
    ],
}