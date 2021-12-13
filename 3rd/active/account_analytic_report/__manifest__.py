# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

{
    'name': 'Analytic Account Report',
    'version': '1.0',
    'summary': 'Analytic Account Report',
    'category': 'Accounting',
    'sequence': 1,
    'description': """
Analytic Account Report

    """,
    'author': 'Synconics Technologies Pvt. Ltd.',
    'website': 'http://www.synconics.com',
    'depends': ['account'],
    'demo': [
    ],
    'data': [
        'wizard/analytic_report_view.xml',
        'views/analytic_template.xml'
    ],
    'images': [
        'static/description/main_screen.jpg',
    ],
    'price': 40,
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'OPL-1',
}
