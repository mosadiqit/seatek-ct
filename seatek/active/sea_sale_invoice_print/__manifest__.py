# -*- coding: utf-8 -*-
{
    'name': "SeaCorp Sale Invoice Print",

    'summary': """
        Phiếu Xuất Kho Theo Hoá Đơn""",

    'description': """
        + Phiếu Xuất Kho Theo Hoá Đơn
        + Phiếu thu
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sale',
    'version': '12.0.0.1.0003',
    # any module necessary for this one to work correctly
    'depends': ['sale', 'account', 'sc_sale_order_line_remarks_field', 'stock_picking_invoice_link', 'sc_stock_report_pdf'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/sea_report_action.xml',
        'report/sea_sale_invoices_delivery_templates.xml',
        'report/sea_invoice_80mm_templates.xml',
        'views/account_invoice_view.xml',
    ],
    # only loaded in demonstration mode
}