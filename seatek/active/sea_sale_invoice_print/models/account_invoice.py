from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
from odoo.addons.global_seatek import Seatek
import decimal

class AccountInvoice(models.Model, Seatek):
    _inherit = 'account.invoice'

    @api.multi
    def get_picking_to_string(self):
        s = ""
        for p in self.picking_ids:
            s += "," + p.name
        if len(s) > 1:
            return s[1:]
        return ""

    @api.multi
    def get_sale_order(self):
        order_id = self.invoice_line_ids.mapped('sale_line_ids').mapped('order_id')
        if order_id is False or order_id is None or order_id.id is False:
            order_id = self.env['sale.order'].search([('name', 'like', self.origin), ('company_id', '=', self.company_id.id)])
            if order_id is False or order_id is None or order_id.id is False:
                order_id = False
        return order_id

    # @api.multi
    # def readNum(self, num):
    #     return readFreeNum(int(num))
    #
    # @api.multi
    # def formatNum(self, num):
    #     return format_number(num)


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    remarks = fields.Text(string='Remarks', store=True, default=False, readonly=False)
    sea_qty_done = fields.Float('Quantity done', copy=False, digits=dp.get_precision('Product Unit of Measure'),
                                default=0.0, compute='_compute_sea_qty_done')

    @api.multi
    @api.depends('move_line_ids.quantity_done')
    def _compute_sea_qty_done(self):
        for line in self:
            # print(line.invoice_id.number)
            # print(line.move_line_ids.product_id.name)
            # qty_done = 0
            # for l in line.move_line_ids:
            #     qty_done = l.quantity_done
            line.sea_qty_done = line.sale_line_ids.qty_delivered
