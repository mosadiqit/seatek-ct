# -*- coding: utf-8 -*-
{
    'name': "Sea Pegasus Delivery Note - PDF",

    'summary': """
        Pegasus Delivery Note Print PDF""",

    'description': """
        Pegasus Delivery Note Print PDF
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sale',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/pegasus_delivery_note_action.xml',
        'report/pegasus_delivery_note_template.xml',

    ],
    'css': [
        'static/src/css/font.css',
    ],
    # only loaded in demonstration mode
}