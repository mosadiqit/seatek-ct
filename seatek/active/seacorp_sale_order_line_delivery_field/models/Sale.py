from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = ['sale.order.line']

    delivery = fields.Text(string='Delivery', store=True, default="")

    @api.multi
    @api.onchange('product_uom_qty', 'product_id')
    def _compute_delivered_method(self):
        for line in self:
            if line.product_id.type == 'product':
                if line.product_uom_qty <= line.product_id.virtual_available:
                    line.delivery = 'Stock'
                else:
                    line.delivery = 'Out of Stock'
            else:  # service and consu
                line.delivery = ''
