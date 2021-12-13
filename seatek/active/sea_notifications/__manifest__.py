# -*- coding: utf-8 -*-
{
    'name': "Email notification Sales Order Confirm",
    'summary': """Email notification Sales Order Confirm""",
    'description': """
        Email notification Sales Order Confirm
    """,
    'website': 'http://www.seacorp.vn',
    'category': 'Seacorp',
    'author': 'DuyBQ',
    'version': '1.0.2',
    'depends': [
        'base',
        'sale_management',
        'sea_menu_base',
        ],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_data.xml',
        'views/notification_view.xml',
        'views/res_config.xml',
        'views/sale_view_order_form.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
