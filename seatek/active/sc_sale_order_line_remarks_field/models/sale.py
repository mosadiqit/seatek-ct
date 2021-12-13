from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    remarks = fields.Text(string='Remarks', store=True, default="")
