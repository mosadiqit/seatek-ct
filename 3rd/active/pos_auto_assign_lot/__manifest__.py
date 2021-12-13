# -*- coding: utf-8 -*-
{
    'name': 'POS | Auto Assign Lot/Serial Numbers',
    'version': '1.0',
    'category': 'Point Of Sale',
    'author':'Craftsync Technologies',
    'maintainer': 'Craftsync Technologies',
    'summary': 'Auto Select required Lots/Serial Numbers when creating POS Order',
    'website': 'https://www.craftsync.com/',
    'license': 'OPL-1',
    'support':'info@craftsync.com',
    'sequence': 1,
    'depends': [
        'point_of_sale','stock'
    ],
    'data': [
       'views/assets.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/main_screen.png'],
    'price': 29.00,
    'currency': 'EUR',
}
