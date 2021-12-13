# -*- coding: utf-8 -*-
{
    'name': "Sea Extend Customer Invoice",

    'summary': """
        Extend model account.invoice""",

    'description': """
        Seacorp them 2 field: số hóa đơn đõ, mã số quyết toán to AR invoice
    """,

    'author': "Seatek",
    'website': "https://seacorp.vn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'accounting',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/SeaInvoice.xml'
    ],
}