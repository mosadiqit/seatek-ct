from odoo import models, fields, api
from odoo.addons.sale_stock.models.sale_order import SaleOrder


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def write(self, values):
        res = super(SaleOrder, self).write(values)
        if 'order_line' in values:
            order_line = values['order_line']
            if order_line:
                for pick in self.picking_ids:
                    if pick.picking_type_id.code == 'outgoing':
                        for line in order_line:
                            vals = line[2]
                            if vals and  'remarks' in vals:
                                move = self.env['stock.move'].search([('picking_id', '=', pick.id), ('sale_line_id', '=', line[1])])
                                if move:
                                    move.write({'remarks': vals['remarks']})
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    remarks = fields.Text(string='Remarks', store=True, default="")
