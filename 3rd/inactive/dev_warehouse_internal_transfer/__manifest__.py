# -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Devintelle Solutions (<http://devintellecs.com/>).
#
##############################################################################
{
    'name': 'Warehouse Internal Transfer Stock',
    'version': '12.0.1.0',
    'sequence':1,
    'category': 'Stock',
    'description': """
        odoo application will to transfer stock one warehouse to second warehouse

    Odoo inter transfer 
    odoo warehouse internal transfer 
    odoo Internal transfer 
    Odoo internal transfer 
    Odoo stock transfer 
    odoo send stock to warehouse 
    odoo receive stock to warehouse 
    odoo stock receive stock notes
    odoo stock send stock notes
    odoo stock moves warehouse 
    odoo warehouse stock moves 


        """,
    'summary': 'odoo Applicatation allow to Transfer Stock one warehouse to another warehouse',
    'depends': ['sale_management','stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/ir_sequence_data.xml',
        'edi/mail_template.xml',
        'views/inter_transfer_views.xml',
        'views/stock_warehouse_view.xml',
        'views/res_config_setting_view.xml',
        'report/header_footer.xml',
        'report/report_inter_transfer.xml',
        'report/report_inter_transfer_slip.xml',
        'report/goods_receive_report_template.xml',
        'report/report_menu.xml',
        'wizard/goods_receive_report.xml',
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
    'price':39.0,
    'currency':'EUR',
    #'live_test_url':'https://youtu.be/A5kEBboAh_k',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
