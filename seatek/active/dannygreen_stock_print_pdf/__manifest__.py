# -*- coding: utf-8 -*-
{
    'name': "Dannygreen Inventory print PDF",

    'summary': """
        Phiếu nhập/xuất kho ký gửi""",

    'description': """
        Settings: Inventory -> DannyGreen Form report
        stock picking form -> button dannygreen print:
            + Phiếu nhập kho ký gửi
            + Phiếu xuất kho ký gửi        
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'stock',
    'version': '12.0.0.1.003',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'sc_stock_report_pdf'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/stock_report_action.xml',
        'report/dannygreen_stock_out_inventory_template.xml',
        'report/dannygreen_stock_in_inventory_template.xml',
        'wizard/stock_report_selection_view.xml',
        'views/stock_picking_views.xml',
        'views/res_config_settings_views.xml'
    ],
}