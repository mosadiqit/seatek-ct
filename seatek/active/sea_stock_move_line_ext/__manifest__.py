# -*- coding: utf-8 -*-
{
    'name': "Stock Move Line Extension",
    'summary': """
        Module extension for Stock""",

    'description': """
        Module extension for Stock:
            - Add Source document on report stock_move_line
            - Add report view stock move line
    """,
    'author': "DuyBQ",
    'website': "https://seacorp.vn",
    'category': 'Seacorp',
    'version': '2.0.1',
    'depends': ['base', 'stock'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/view_move_line_tree_inherit.xml',
        'views/stock_move_line_report_ext.xml',
    ],
}