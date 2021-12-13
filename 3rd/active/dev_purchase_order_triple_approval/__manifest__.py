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
    'name': 'Purchase Tripple Approval Process',
    'version': '12.0.1.1',
    'sequence': 1,
    'category': 'Purchases',
    'description':
        """
        This module helps you to set limit on Purchase Orders, So, Manager must have validate Purchase Order if it exceed the Per-Defined Limit before Confirmation.
         -- will be two step or three step Approval based on conditions
         
         purchase approval, approval, Purchase Third validation, Purchase validation, Purchase two step , Purchase three step, Purchase step approval, Purchase double approval,  
purchase Order Triple Approval
Odoo purchase Order Triple Approval
purchase approval 
Odoo purchase approval
purchase triple approval 
Odoo purchase triple approval 
purchase double approval 
Odoo purchase double approval
odoo app will help you to add tripple approval confirmation process in purchase order process.
Set Three Step Verification on purchase Orders
Odoo Set Three Step Verification on purchase Orders
Set a limit amount on purchase Order as double and trippe Step Verification
Odoo Set a limit amount on purchase Order as double and trippe Step Verification
Manage three set verification on purchase orders
Odoo manage three set verification on purchase orders
purchase order approval 
Odoo purchase order approval 
purchase order approval 
Odoo purchase order approval 
Manage purchase order approval 
Odoo manage purchase order approval
purchase order double approval 
Odoo purchase order double approval 
Manage purchase order triple approval 
Odoo manage purchase order triple approval 
Create purchase approval 
Odoo create purchase approval 
Create purchase double approval 
Odoo create purchase double approval 
Create purchase triple approval 
Odoo create purchase triple approval
    """,
    'summary': 'odoo Purchase Tripple Approval Process- third level Approval in purchase order with Purchase managers, users',
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com/',
    'depends': ['base', 'purchase'],
    'data': [
        'security/security.xml',
        'views/res_config_settings_views.xml',
        'views/purchase_order_view.xml',
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
    'price':39.0,
    'currency':'EUR',
   # 'live_test_url':'https://youtu.be/A5kEBboAh_k',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
