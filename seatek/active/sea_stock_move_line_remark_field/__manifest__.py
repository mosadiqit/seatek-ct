# -*- coding: utf-8 -*-
{
    'name': "Sea Stock Move Line Remark Field",
    'summary': """
        Module extension for Stock""",

    'description': """
        Module extension for Stock:
            - Add Source document on report stock_move_line_remark_field
            
    """,
    'author': "Seatek",
    'website': "https://seacorp.vn",
    'category': 'stock',
    'version': '12.0.0.1',
    'depends': ['base', 'stock', 'sale_stock'],
    'data': [
        'views/view_move_line_remark_inherit.xml',

    ],
}