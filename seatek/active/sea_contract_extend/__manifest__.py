# -*- coding: utf-8 -*-
{
    'name': 'Open Sea Contract Extend',
    'version': '12.0.0.0.1',
    'summary': """Open Sea Contract Extend""",
    'description': 'Open Sea Contract Extend.',
    'category': 'Open Sea Contract Extend',
    'author': 'Nam',
    'company': 'Seacorp',
    'website': "https://www.seacorp.com",
    'depends': ['base', 'hr', 'mail', 'hr_gamification', 'hr_contract', 'note'],
    'data': [
        'security/ir.model.access.csv',
        'views/sea_contract_extend.xml',
    ],
    'demo': [],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
