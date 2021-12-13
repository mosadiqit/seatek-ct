# -*- coding: utf-8 -*-
{
    'name': "Sea SeaFarm Stock Report PDF",
    'summary': "Sea SeaFarm Stock Report PDF",
    'description': """ 
        Sea SeaFarm Stock Report PDF
    """,
    'author': "SeaTek",
    'website': "https://www.seacorp.vn",
    'category': 'stock',
    'version': '12.0.0.0',
    'depend': ['base', 'stock', 'sale', 'sc_stock_report_pdf'],
    'data': [
        'report/action_report.xml',
        'report/sea_farm_import_template.xml',
        'report/sea_farm_export_template.xml',
        'report/sea_farm_equipment_handover_template.xml',
        'report/sea_farm_receipt_template.xml',
        'report/sea_farm_delivery_bill_template.xml',
    ],
    'installable': True,
    'application': False,
}