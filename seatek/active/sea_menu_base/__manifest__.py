# -*- coding: utf-8 -*-
{
    'name': "Report menu Extension",
    'summary': """Report Extension menu""",
    'description': """
        1.0.2:
            + Add Menu for all custom report
        1.0.3:
            + Add menuitem 'Warehouse' in file menuitem_base.xml
    """,
    'website': 'http://www.seacorp.vn',
    'category': 'Seacorp',
    'author': 'DuyBQ',
    'version': '1.0.4',
    'depends': ['web'],
    'data': [
        'security/ir.model.access.csv',
        'views/menuitem_base.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
