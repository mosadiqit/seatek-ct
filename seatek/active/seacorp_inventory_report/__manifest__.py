# -*- coding: utf-8 -*-
{
    "name": "Seacorp Inventory Report",
    "summary": "Báo cáo xuất nhập tồn",
    "version": "12.0.1.0.15",
    "category": "stock",
    "website": "https://trinhgialac.com",
    "author": "TGL team",
    "license": "AGPL-3",
    "depends": [
        "stock"
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/inventory_report.xml'
    ],
    "images": ["static/description/icon.png"],
    "application": False,
    "installable": True,
}
