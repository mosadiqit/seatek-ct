# -*- coding: utf-8 -*-
{
    'name': "Sea Pegasus Sale Quotation - PDF",

    'summary': """
        Pegasus sale quotation order report PDF""",

    'description': """
        Pegasus sale quotation order report PDF
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

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
        'report/pegasus_sale_quotation_action_report.xml',
        'report/pegasus_sale_quotation_template_pdf.xml',
    ],
    'installable': True,
    'application': False,
}