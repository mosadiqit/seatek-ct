# -*- coding: utf-8 -*-

{
    'name': 'SeaCorp Purchase Order Extend Report',
    'version': '12.0.0.1',
    'category': 'Purchases',
    'summary': 'SeaCorp Purchase Order Extend Report',
    'description': "SeaCorp Purchase Order Extend Report",
    'website': 'www.seatek.vn',
    'author': 'SeaTek',
    'depends': ['base', 'purchase'],
    'data': [
        'report/purchase_report_action.xml',
        'report/dannygreen_purchase_order_report.xml',
            ],
    'installable': True,
    'auto_install': False,
    'application': True,
}