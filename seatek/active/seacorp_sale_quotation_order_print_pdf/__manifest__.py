# -*- coding: utf-8 -*-
{
    'name': "Seacorp Sale Quotation print PDF",

    'summary': """
        Seatek Sale Quotation print PDF""",

    'description': """
        Seatek Sale Quotation print PDF
    """,

    'author': "Seatek",
    'website': "http://www.yourcompany.com",

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
        'report/pegasus_sale_quotation_order_template.xml',
        'report/seacorp_sale_quotaion_order_report.xml',
        'views/res_config_settings_views.xml'
    ],
    'css': [
        'static/src/css/font.css',
    ],
    # only loaded in demonstration mode
}