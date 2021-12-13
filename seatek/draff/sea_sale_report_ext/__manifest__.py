# -*- coding: utf-8 -*-
{
    'name': 'Sale Order Line Extension',
    'author' : 'DuyBQ',
    'website': 'https://www.seacorp.vn',
    'version': '2.0.1',
    'category': 'seacorp',
    'summary': 'This module Report extension for SaleOrder lines.',
    'description': """This module Report extension for SaleOrder lines.
        - Show other information related:
            + List View
            + Form View
            + Kanban View
            + Search View
    """,
    'depends': ['sale_management'],
    'data': [
        'views/sale_order_line.xml',
        'views/web_assets_backend.xml',
        'security/ir.model.access.csv',
    ],
    'qweb': [
        "static/src/xml/update_view.xml",
    ],
    'auto_install': False,
    'installable' : True,
    'application': True,     
}
