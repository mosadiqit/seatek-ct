# -*- coding: utf-8 -*-
{
    'name': "Sea Stock In/Out By Location",

    'summary': """
        Seacorp Inventory report view
        """,

    'description': """
        Menu : OpenSea->Inventory-> Stock In/Out By Location  ( Báo cáo XNT Tổng Hợp Theo Kho)
        Start Date: Ngày lấy Dữ liệu Bắt Đầu ( theo dữ liệu Stock Move ) - từ 0.00 ngày Start Date
        To Date: Ngày Lấy Dữ liệu  Kết Thúc  ( tới 12:00 PM To Date )
        Chọn sẵn Range : Today, This Month, This Week, Last Day, Last Month , Last Week

        Stock Picking/Date of Transfer
        Location : chọn nhiều Location , không chọn -> lấy All
        Product: Chọn nhiều Product , không chọn -> Lấy All
        Category : Chọn nhiều Product Category, không chọn lấy All.
        
        Hiển thị dạng List View ( như báo cáo hiện thời )
        Filter:
        Closing Positive Stock -> chỉ hiển thị  Closing > 0
        Closing Negative Stock -> chỉ hiển thị  Closing < 0
        Opening Positive Stock -> chỉ hiển thị  Opening > 0
        Opening Negative Stock -> chỉ hiển thị  Opening <  0
        Group By : Location, Product, Unit -> các số qty Sum theo Group
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'stock',
    'version': '12.0.0.1.00002',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'product', 'mrp'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
        'views/sea_stock_quantity_history.xml',
        'wizard/sea_view_stock_product_tree.xml',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'application': False,
    'auto_install': False,
}