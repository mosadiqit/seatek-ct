# -*- coding: utf-8 -*-
{
    'name': "Sea Purchase Line Extend",

    'summary': """
        Seacorp add HS Code field to purchase order line và enable field source Document trên header,
	Thêm 1 fied ghi tên con tàu""",

    'description': """
        Seacorp add HS Code field to purchase order line và enable field source Document trên header
	Thêm 1 fied ghi tên con tàu
    """,

    'author': "Seatek",
    'website': "https://seacorp.vn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'purchase',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sea_purchase_order_line.xml'
    ],
}