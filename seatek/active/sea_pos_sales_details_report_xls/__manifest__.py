# -*- coding: utf-8 -*-
{
    'name': "Sea Pos Sales Details Report - XLS",

    'summary': """
       Sea Pos Sales Details Report - XLS""",

    'description': """
        Sea Pos Sales Details Report - XLS
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

    'category': 'Point of Sale',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'pos_retail', 'point_of_sale', 'report_xlsx_helper', 'report_xlsx'],

    # always loaded
    'data': [
        'report/sales_details_view.xml',
    ],
}
