# Copyright 2019 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'SeaTek Stock Card Report',
    'summary': 'Add stock card report on Inventory Reporting.',
    'version': '12.0.1.0.2',
    'category': 'Warehouse',
    'website': 'https://github.com/OCA/stock-logistics-reporting',
    'description': """
        12.0.1.0.1:
            + Convert to sea_stock_card_report 
        12.0.1.0.2: 
            + Get data in stock_move_line
         12.10.1.0.3 : Nov252020 Checked  

    """,
    'author': 'Ecosoft,Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'depends': [
        'stock',
        'date_range',
        'report_xlsx_helper',
        'sea_menu_base'
    ],
    'data': [
        'data/paper_format.xml',
        'data/report_data.xml',
        'reports/stock_card_report.xml',
        'wizard/stock_card_report_wizard_view.xml',
    ],
    'installable': True,
}
