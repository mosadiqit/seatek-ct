# -*- coding: utf-8 -*-
{
    'name': "Dannygreen Invoicing print PDF",

    'summary': """
        Dannygreen Invoicing print PDF""",

    'description': """
        Settings: Invoices/Account -> DannyGreen Form report
        Invoice form -> button dannygreen print:
            + Phiếu bán hàng ky Gửi
            + Phiếu xuất kho kiêm giao nhận
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'account',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/dannygreen_account_invoicing_sale_slip_template.xml',
        'report/dannygreen_account_invoicing_xuat_kho_giao_nhan_template.xml',
        'report/account_report_action.xml',
        'wizard/dannygreen_account_invoicing_selection_report_view.xml',
        'views/account_invoicing_views.xml',
        'views/res_config_settings_views.xml'
    ],
}