# -*- coding: utf-8 -*-
{
    'name': "Sea Stock PDF Reports",

    'summary': """
        stock picking in/out export""",

    'description': """
        stock picking in/out export
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'stock',
    'version': '12.0.0.2.4',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'sale', 'sc_stock_report_pdf'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/sc_in_out_report_template.xml',
        'report/sc_stock_sale_delivery_templates.xml',
        'report/sc_stock_internal_transfer_template.xml',
        'report/sc_stock_internal_transfer_template_add.xml',
        'report/sc_stock_internal_transfer_template_out.xml',
        'report/seatek_report_action.xml',
        'report/sc_stock_sale_withdraw_templates.xml'
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': False,
}
