# -*- coding: utf-8 -*-
{
    'name': "Sea Pegasus PRO-FORMA Invoice - PDF",

    'summary': """
        Pegasus Proforma Invoice - PDF""",

    'description': """
        Pegasus Proforma Invoice - PDF
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sale',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctlys
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/pegasus_proforma_invoice_action_report.xml',
        'report/pegasus_proforma_invoice_template.xml',
    ],
    'installable': True,
    'application': False,
}