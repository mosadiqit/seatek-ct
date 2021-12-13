# -*- coding: utf-8 -*-
{
    'name': "Report XLS - Extension",
    'summary': """
        Export data to file excel""",
    'description': """
        General report Excel/CSV
            + POS Session Report
        12.0.0.2:
            + Add Remarks field, stock_report_xls.xml
        12.0.0.3:
            + Thêm cột "Số trái", "Lot" trong file stock_report_xls.py
        12.0.0.4:
            + Thêm cột "Giá bán", "Thành tiền giá bán" trong file stock_report_xls.py
        
    """,
    'author': "DuyBQ",
    'website': "http://www.seacorp.vn",
    'category': 'Seacorp',
    'version': '12.0.0.4',
    'depends': ['report_xlsx',
                # 'report_csv',
                'sea_menu_base',
                # 'point_of_sale',
                'sale',
                'stock',
                
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_report.xml',
        # 'reports/pos_session/pos_session_wizard.xml',
        'reports/sale_order/sale_order_wizard.xml',
        'reports/stock_report/stock_report_wizard.xml',
    ],
    'installable': True,
    'auto_install': False,
}
