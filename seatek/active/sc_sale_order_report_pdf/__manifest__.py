# -*- coding: utf-8 -*-
{
    'name': "Seacorp Sale Order report PDF",

    'summary': """
       Seacorp Sale Order report PDF""",

    'description': """
        Sale Order - Đơn Đặt Hàng
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sale',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/sale_order_templates.xml',
        'report/sale_report.xml',
    ],
}