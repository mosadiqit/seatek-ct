# -*- coding: utf-8 -*-
{
    'name': "Sea Pegasus PRO-FORMA Invoice - XLS",

    'summary': """
       Pegasus PROFORMA Invoice Report - XLS""",

    'description': """
        Pegasus PROFORMA Invoice Report - XLS
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

    'category': 'sale',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [

        'reports/proforma_invoice_report.xml',
    ],
}
