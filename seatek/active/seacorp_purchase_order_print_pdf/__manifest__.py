# -*- coding: utf-8 -*-
{
    'name': "Seacorp Purchase Order Print PDF",

    'summary': """
        Seacorp Purchase Order Print PDF""",

    'description': """
        Seacorp Purchase Order Print PDF
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

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
        'report/pegasus_purchase_order_template.xml',
        'report/seacorp_purchase_order_report.xml',
        'views/res_config_settings_views.xml',
    ],
    'css': [
        'static/src/css/font.css',
    ],
    # only loaded in demonstration mode
}