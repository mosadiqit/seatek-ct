from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = "stock.move"


class StockPicking(models.Model):
    _inherit = "stock.picking"

    currency_id = fields.Many2one('res.currency', 'Currency', readonly=True,
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all')

    @api.depends('move_lines.price_total')
    def _amount_all(self):
        for picking in self:
            amount_total = 0.0
            for line in picking.move_lines:
                amount_total += line.price_total
            picking.update({
                'amount_total': amount_total,
            })
