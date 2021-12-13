# -*- coding: utf-8 -*-
#╔══════════════════════════════════════════════════════════════════╗
#║                                                                  ║
#║                ╔═══╦╗       ╔╗  ╔╗     ╔═══╦═══╗                 ║
#║                ║╔═╗║║       ║║ ╔╝╚╗    ║╔═╗║╔═╗║                 ║
#║                ║║ ║║║╔╗╔╦╦══╣╚═╬╗╔╬╗ ╔╗║║ ╚╣╚══╗                 ║
#║                ║╚═╝║║║╚╝╠╣╔╗║╔╗║║║║║ ║║║║ ╔╬══╗║                 ║
#║                ║╔═╗║╚╣║║║║╚╝║║║║║╚╣╚═╝║║╚═╝║╚═╝║                 ║
#║                ╚╝ ╚╩═╩╩╩╩╩═╗╠╝╚╝╚═╩═╗╔╝╚═══╩═══╝                 ║
#║                          ╔═╝║     ╔═╝║                           ║
#║                          ╚══╝     ╚══╝                           ║
#║ SOFTWARE DEVELOPED AND SUPPORTED BY ALMIGHTY CONSULTING SERVICES ║
#║                   COPYRIGHT (C) 2016 - TODAY                     ║
#║                   http://www.almightycs.com                      ║
#║                                                                  ║
#╚══════════════════════════════════════════════════════════════════╝
{
    'name': 'Add Products by Barcode in Stock Operation',
    'version': '1.0',
    'category': 'Inventory Management',
    'author': 'Almighty Consulting Services',
    'support': 'info@almightycs.com',
    'summary': """Add Products by scanning barcode to avoid mistakes and make work faster in Stock Operation.""",
    'description': """Add Products by scanning barcode to avoid mistakes and make work faster in Stock Operation.""",
    'website': 'http://www.almightycs.com', 
    "depends": ["stock"],
    "data": [
        "views/stock_view.xml",
    ],
    'images': [
        'static/description/barcode_cover.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'price': 9,
    'currency': 'EUR',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: