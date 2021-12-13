from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = ['purchase.order.line']

    remarks = fields.Text(string='Remarks', store=True, default="")
