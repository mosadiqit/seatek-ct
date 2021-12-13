# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################
{
    'name': 'Product Stocks By locations & Report',
    'version': '12.0.1.0',
    'sequence': 1,
    'category': 'Warehouse',
    'description':
        """ 
        This Apps add below functionality into odoo 
        
        1.This module helps you to show stock by Location
Product Stocks By locations & Report
Odoo Product Stocks By locations & Report
Product stocks by location 
Odoo product stocks by location 
Manage product stocks 
Odoo manage product stocks 
Product stocks by report 
Odoo product stocks by report 
Manage product stocks by location 
Odoo manage product stocks by location 
Manage product stocks by report 
Odoo manage product stocks by report 
Filter by Start date and End date. Fetch stock by location from date and to date
Odoo Filter by Start date and End date. Fetch stock by location from date and to date
Track Stock By Location Of Product and Product Variant
Odoo Track Stock By Location Of Product and Product Variant
 In Single Click Print Stock By Location Report
Odoo  In Single Click Print Stock By Location Report
Product variant stock by location 
Odoo product variant stock by location 
Manage Product variant stock by location 
Manage Odoo product variant stock by location 
Manage Product variant stock by report 
Manage Odoo product variant stock by report



        
    """,
    'summary': 'Odoo app shows Stock Quantity for different Location on Product', 
    'depends': ['sale_stock','stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template.xml',
        'report/stock_by_location_report.xml',
        'report/report_menu.xml',
    ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    
    # author and support Details =============#
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',    
    'maintainer': 'DevIntelle Consulting Service Pvt.Ltd', 
    'support': 'devintelle@gmail.com',
    'price':14.0,
    'currency':'EUR',
    #'live_test_url':'https://youtu.be/A5kEBboAh_k',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
