# -*- coding: utf-8 -*-
{
    'name': 'Open Sea Employee Extend',
    'version': '12.0.0.0.0',
    'summary': """Extend Employee OpenSea""",
    'description': 'Extend Employee OpenSea.',
    'category': 'Extend Employee OpenSea',
    'author': 'Nam',
    'company': 'Seacorp',
    'website': "https://www.seacorp.com",
    'depends': ['base', 'hr', 'mail', 'hr_gamification', 'sea_menu_base', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_view.xml',
        'views/hr_notification.xml',
        'wizard/opensea_employee_list.xml',
    ],
    'demo': [],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
