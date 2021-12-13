# -*- coding: utf-8 -*-
{
    'name': 'Delivery receipt',
    'version': '12.0.1.0.4',
    "sequence": 5,
    'category': 'point_of_sale',
    'author': 'Trình Gia Lạc',
    'website': 'https://trinhgialac.com',
    'summary': 'Bản in 80mm trên SO dựa theo số lượng giao',
    'description': """
        Bản in 80mm trên SO dựa theo số lượng giao
    """,
    'depends': ['sale_stock'],
    'data': [
        'report/paper_format.xml',
        'report/template_report.xml',
        'views/warehouse_view.xml',
    ],
}
