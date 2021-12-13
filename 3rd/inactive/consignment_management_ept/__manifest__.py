# -*- coding: utf-8 -*-
{
        # App information
        'name': 'Consignment Management',
        'version':  '12.0',
        'category': 'Sales',
        'summary':  'Consignment process is keeping the stock in customers premises, but until the customer consumes or sell it, it will be a part of the company. Consignment stock can be at the customers premises or it can be in the company premises too.',
        'license': 'OPL-1',
        
        # Author
        'author': 'Emipro Technologies Pvt. Ltd.',
        'website': 'http://www.emiprotechnologies.com',
        'maintainer': 'Emipro Technologies Pvt. Ltd.',
        
        # Dependencies
        'depends':['sale_stock','sale_management'],
        
        # Views
        'data':[    
            'data/ir_sequence_data.xml',
            'security/consignment_management_security.xml',
            'security/ir.model.access.csv',
            'views/view_res_partner_ept.xml',
            'views/view_product_product_ept.xml',
            'views/view_stock_warehouse_ept.xml',
            'views/view_sale_order_ept.xml',
            'views/view_menu_consignment_management_ept.xml',
            'views/view_consignment_process_ept.xml',
            'views/view_consignment_return_ept.xml',
            'views/view_consignee_to_consignee_ept.xml',
            'views/view_consignment_log_ept.xml',
            
            'wizard/import_consignment_transactions.xml',
            
            'report/view_consignment_stock_report_ept.xml',
            'report/consignment_stock_report_pdf.xml',
            
            
                ],
                
         # Odoo Store Specific
		'images': ['static/description/Consignment-Management-Cover.jpg'],         
        
        'installable': True,
        'application': True,
        'auto_install': False,
        'post_init_hook': 'create_default_warehouse',
	    'live_test_url':'https://www.emiprotechnologies.com/free-trial?app=consignment-management-ept&version=12&edition=enterprise',
		'price': '499',
		'currency': 'EUR',		
}
