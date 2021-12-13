from odoo import models, fields, api
from odoo.addons.global_seatek import Seatek

class SaleOrder(models.Model, Seatek):
    _inherit = "sale.order"

    # total_discount = fields.Monetary(string='Amount discount', readonly=True,
    #                                  help="Total amount discount", store=True, compute='_compute_total_amount_qty_delivery')
    total_amount_qty_delivery = fields.Monetary(string='*Delivered Amount', readonly=True,
                                                help="Total amount Qty Delivery", store=True,
                                                compute='_compute_total_amount_qty_delivery')

    @api.multi
    @api.depends('order_line.sea_price_total_qty_delivered')
    def _compute_total_amount_qty_delivery(self):
        for s in self:
            total = 0
            # total_discount = 0
            for line in s.order_line:
                total += line.sea_price_total_qty_delivered
                # total_discount += line.price_discount
            s.update({
                'total_amount_qty_delivery': total,
                # 'total_discount': total_discount
            })

    def get_commitment_date(self):
        if self.commitment_date:
            return self.commitment_date.strftime("Ngày %d tháng %m năm %Y")
        return ""


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # price_discount = fields.Monetary(string='Price discount',
    #                                  store=True,
    #                                  help="Price discount", compute='_compute_amount_qty_delivered')
    # price_total_without_discount = fields.Monetary(string='*Delivered Amount Line without discount',
    #                                                store=True,
    #                                                help="Price without discount", compute='_compute_amount_qty_delivered')

    sea_price_total_qty_delivered = fields.Monetary(string='*Delivered Amount Line', store=True,
                                                    help="Price total of line by Delivered qty",
                                                    compute='_compute_amount_qty_delivered')

    @api.multi
    @api.depends('product_uom_qty', 'qty_delivered', 'discount', 'price_unit')
    def _compute_amount_qty_delivered(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            # if line.product_id.invoice_policy == 'delivery':
            #     qty = line.qty_delivered
            # else:
            #     qty = line.product_uom_qty
            # line.price_total_without_discount = qty * line.price_unit
            # line.price_discount = (line.price_total_without_discount * line.discount) / 100
            line.update({
                # 'price_discount': line.price_discount,
                # 'price_total_without_discount': line.price_total_without_discount,
                'sea_price_total_qty_delivered': line.untaxed_amount_to_invoice + line.untaxed_amount_invoiced,
            })
