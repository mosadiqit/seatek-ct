from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    amount_subtotal = fields.Monetary(string='subtotal', store=True, readonly=True, compute='_get_amount_subtotal')

    # @api.depends('order_line.price_subtotal')
    def _get_amount_subtotal(self):
        for sale in self:
            amount_subtotal = 0.0
            for line in sale.order_line:
                amount_subtotal += line.price_subtotal
            sale.update({
                'amount_subtotal': amount_subtotal,
            })
