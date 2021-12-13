# -*- coding: utf-8 -*-
{
    'name': "Account Invoice Extension",
    'summary': """
        Module extension for Account Invoice""",

    'description': """
        Module extension for Account:
            - Add Commit date of Sale order to tree view
    """,
    'author': "DuyBQ",
    'website': "https://seacorp.vn",
    'category': 'Seacorp',
    'version': '1.0.1',
    'depends': ['base', 'stock'],
    'data': [
        'views/account_invoice_tree.xml',
    ],
}