# -*- coding: utf-8 -*-
{
    'name': 'Seacorp POS Receipt',
    'version': '12.0.1.0.1',
    'category': 'Point of Sale',
    'summary': '',
    'description': """

Thêm phí vận chuyển trong POS
==============================
    
    
    Thêm field Enable Shipping cost ở Mục POS config


Subtotal POS Receipt
==============================


    Thêm field Enable Taxes in Receipt ở Page "Receipt and Ticket" trong POS config

Màn hình Order (giao diện POS)
===============================
    

    Thêm field Enable Taxes Percent ở Page "Order and Booking" trong POS config



Thiết kế Biểu mẫu POS Receipt
==============================

    """,
    'depends': ['pos_retail'],
    'author': 'TGL Team',
    'support': 'info@trinhgialac.com',
    'data': [
        'views/pos_config_view.xml',
        'views/pos_templates.xml',
    ],
    'qweb': ['static/src/xml/pos_view.xml'],
    'installable': True,
}
