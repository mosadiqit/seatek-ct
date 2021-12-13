from odoo import fields, models, api, tools, _
from odoo.tools.misc import formatLang


class Warehouse(models.Model):
    _inherit = 'stock.warehouse'

    so_receipt_header = fields.Html('Đầu hóa đơn bán hàng')
    so_receipt_footer = fields.Html('Chân hóa đơn bán hàng')
