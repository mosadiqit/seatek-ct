{
    "name": "Internal transfer two step",
    "summary": "Internal transfer two step",
    "version": "12.0",
    "category": "stock",
    "website": "https://trinhgialac.com",
    "author": "TGL team",
    "license": "AGPL-3",
    "depends": [
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        'wizard/stock_move_location_view.xml',
        "views/stock_warehouse_view.xml",
        "views/stock_picking_view.xml",
        "reports/report_internal_view.xml",
    ],
    "application": False,
    "installable": True,
}
