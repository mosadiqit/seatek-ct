# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class ProductTemplate(models.Model):
#     _inherit = 'product.template'

#     invoice_policy = fields.Selection(selection_add=[
#         ('demand_delivery', 'Invoice what has Initial Demand Delivery'),
#         ('plan_delivery', 'Invoice what has plan Delivery')])


# class ResConfigSettings(models.TransientModel):
#     _inherit = 'res.config.settings'

#     default_invoice_policy = fields.Selection(selection_add=[
#         ('demand_delivery', 'Invoice what has Initial Demand Delivery'),
#         ('plan_delivery', 'Invoice what has plan Delivery')])


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    override_invoice_policy = fields.Boolean('Áp dụng chính sách xuất hóa đơn')
    invoice_policy = fields.Selection([
        ('order', 'SL đặt hàng'),
        ('delivery', 'SL đã giao'),
        # ('demand_delivery', 'Invoice what has Initial Demand Delivery'),
        ('plan_delivery', 'SL dự kiến giao')], string='Theo', default='order')


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('move_ids', 'move_ids.state', 'move_ids.product_uom_qty', 'move_ids.quantity_done')
    def _compute_demand_qty_delivered(self):
        for r in self:
            move_ids = self.env['stock.move'].search([('sale_line_id', '=', r.id), ('state', '!=', 'cancel')])
            r.demand_qty_delivered = sum(
                move_ids.mapped('product_uom_qty'))
            r.plan_qty_delivered = sum(
                move_ids.mapped('quantity_done'))

    demand_qty_delivered = fields.Float(compute='_compute_demand_qty_delivered', store=True)
    plan_qty_delivered = fields.Float(compute='_compute_demand_qty_delivered', store=True)

    @api.depends('qty_invoiced', 'qty_delivered', 'product_uom_qty', 'order_id.state', 'demand_qty_delivered', 'order_id.override_invoice_policy', 'order_id.invoice_policy')
    def _get_to_invoice_qty(self):
        super(SaleOrderLine, self)._get_to_invoice_qty()
        for line in self:
            order_id = line.order_id
            if order_id.state != 'cancel':
                if order_id.override_invoice_policy:
                    if order_id.invoice_policy == 'order':
                        line.qty_to_invoice = line.product_uom_qty - line.qty_invoiced
                    elif order_id.invoice_policy == 'delivery':
                        line.qty_to_invoice = line.qty_delivered - line.qty_invoiced
                    elif order_id.invoice_policy == 'demand_delivery':
                        line.qty_to_invoice = line.demand_qty_delivered - line.qty_invoiced
                    elif order_id.invoice_policy == 'plan_delivery':
                        line.qty_to_invoice = line.plan_qty_delivered - line.qty_invoiced
                elif line.product_id.invoice_policy == 'demand_delivery':
                    line.qty_to_invoice = line.demand_qty_delivered - line.qty_invoiced
                elif line.product_id.invoice_policy == 'plan_delivery':
                    line.qty_to_invoice = line.plan_qty_delivered - line.qty_invoiced
