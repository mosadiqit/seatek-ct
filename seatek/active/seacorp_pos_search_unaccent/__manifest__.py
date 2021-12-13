# -*- coding: utf-8 -*-
{
    'name': 'Seacorp POS search with unaccent',
    'version': '12.0.1.0.2',
    'category': 'Point of Sale',
    'summary': 'Hỗ trợ tìm tên khách hàng và tên sản phẩm không dấu',
    'description': """

Hỗ trợ tìm tên khách hàng và tên sản phẩm không dấu
12.0.1.0.2 : NTC add partner name empty case
-----------------------------------------------------

Trong backend
---------------

    Hiển thị SĐT trong lúc tìm khách hàng 

    Tìm khách hàng bằng số điện thoại trong


    """,
    'depends': ['pos_retail'],
    'author': 'TGL Team',
    'support': 'info@trinhgialac.com',
    'data': [
        'views/pos_templates.xml',
    ],
    'qweb': [],
    'installable': True,
}
