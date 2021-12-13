# -*- coding: utf-8 -*-
{
    'name': "Seacorp Stock Report PDF",

    'summary': """
        stock picking in/out report""",

    'description': """
        12.0.0.1.1
            Stock picking form -> print:
                + Phiếu xuất kho kiêm giao nhận
                + Phiếu chuyển/nhập/xuất kho
        12.0.0.1.0008
            - sửa "Nhà cung cấp" trong file sc_stock_internal_transfer_template.xml
        12.0.0.2.2
            - sửa phiếu chuyển kho 
        12.0.0.2.3
            - Thêm "Phiếu xuất kho", "Phiếu nhập kho"
        
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'stock',
    'version': '12.0.0.2.4',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order_views.xml',
    ],
    # only loaded in demonstration mode

}