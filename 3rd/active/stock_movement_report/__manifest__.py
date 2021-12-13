# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Inventory Movement Report (Onscreen, Excel and PDF)',
    'version': '1.0',
    'category': 'Warehouse',
    'summary': 'Inventory Movement Report (Onscreen, Excel and PDF)',
    'depends': ['stock_account'],
    'author': 'Synconics Technologies Pvt. Ltd.',
    'website': 'http://www.synconics.com',
    'description': """ Inventory movement report
    
    stock
    inventory
    movement
    report
    warehouse
    Inventory Movement Report (Onscreen, Excel and PDF)
inventory
inventory movement
report
summary
inventory report
onscreen report
onscreen summary
inventory forecast
inventory transfer
inventory excel report
inventory pdf report
inventory onscreen report
inventory status report
inventory status
inventory valuation
incoming inventory
outgoing inventory
closing inventory
fiscal year
fiscal year inventory
fiscal year inventory report
date range
date range inventory report
company wise inventory report
company wise inventory status
inventory quantity report
inventory quantity status
product filter
product category filter
stock report
stock pdf report
stock excel report
pdf report
excel report
stock onscreen report
stock status report
stock valuation
incoming stock
outgoing stock
closing stock
fiscal year stock
fiscal year stock report
date range stock report
company wise stock report
company wise stock status
company wise product
company wise product status
item report
onscreen item report
pdf item report
excel item report
item status report
incoming item
outgoint item
closing item report
fiscal year item report
onscreen pdf
onscreen xls
    
""",
    'data': [
        'views/assets_registry.xml',
        'views/inventory_movement_report_views.xml',
        'views/res_config_settings_views.xml',
        'report/report_inventory_movement_templates.xml',
    ],
    'images': ['static/description/main_screen.png'],
    'qweb': ['static/src/xml/*.xml'],
    'price': 149.0,
    'currency': 'EUR',
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'OPL-1',
}
