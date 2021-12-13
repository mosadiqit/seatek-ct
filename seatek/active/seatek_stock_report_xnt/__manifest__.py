# -*- coding: utf-8 -*-
{
    "name": "SeaTek Inventory Report",
    "summary": "Báo cáo xuất nhập tồn",
    "version": "12.0.1.0.3",
    "category": "stock",
    "website": "https://trinhgialac.com",

    "author": "TGL team",
    "license": "AGPL-3",
    "depends": [
        "stock",
        "report_xlsx",
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/inventory_report.xml',
        'reports/report_xlsx.xml',
    ],
    "images": ["static/description/icon.png"],
    "application": False,
    "installable": True,
}
