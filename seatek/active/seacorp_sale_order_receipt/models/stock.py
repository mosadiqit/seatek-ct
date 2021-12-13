from odoo import fields, models, api, tools, _
from odoo.tools.misc import formatLang

class StockMove(models.Model):
    _inherit = 'stock.move'

    sale_price_unit = fields.Float(related='sale_line_id.price_unit', store=True)
    tax_id = fields.Many2many('account.tax', 'stock_move_tax_rel', 'stock_move_id', 'tax_id', related='sale_line_id.tax_id', store=True)
    price_subtotal = fields.Monetary(compute='_compute_sale_info_value', compute_sudo=True, string='Subtotal', readonly=True, store=True)
    price_tax = fields.Float(compute='_compute_sale_info_value', compute_sudo=True, string='Total Tax', readonly=True, store=True)
    price_total = fields.Monetary(compute='_compute_sale_info_value', compute_sudo=True, string='Total', readonly=True, store=True)
    discount = fields.Float(related='sale_line_id.discount', store=True)
    discount_value = fields.Float(compute='_compute_sale_info_value', compute_sudo=True, store=True)
    currency_id = fields.Many2one(related='sale_line_id.currency_id', store=True)

    @api.depends('quantity_done', 'discount', 'sale_price_unit', 'tax_id')
    def _compute_sale_info_value(self):
        for line in self:
            price = line.sale_price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.currency_id, line.quantity_done, product=line.product_id, partner=line.sale_line_id.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'discount_value': line.sale_price_unit * line.quantity_done * line.discount / 100.0,
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    def get_taxes_value(self):
        res = {}
        for line in self:
            price = line.sale_price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.currency_id, line.quantity_done, product=line.product_id, partner=line.sale_line_id.order_id.partner_shipping_id)
            for tax in taxes['taxes']:
                res.setdefault(tax['name'], 0)
                res[tax['name']] += tax['amount']
        return res
