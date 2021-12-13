# -*- coding: utf-8 -*-
{
    'name': 'OpenSea Employee Extend 2',
    'version': '12.0.0.0.2',
    'summary': """Extend Employee OpenSea""",
    'description': 'Extend Employee OpenSea.',
    'category': 'Extend Employee OpenSea',
    'author': 'Nam',
    'company': 'Seacorp',
    'website': "https://www.seacorp.com",
    'depends': ['base', 'hr', 'mail', 'sea_menu_base', 'report_xlsx'],
    'data': [
         'views/hr_employee_view.xml',
         'security/ir.model.access.csv',
    ],
    'demo': [],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
