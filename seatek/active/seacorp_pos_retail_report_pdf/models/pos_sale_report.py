# -*- coding: utf-8 -*-

from odoo import models, fields, api


class pos_sale_report(models.TransientModel):
    _inherit = 'pos.sale.report'
    _description = "Report of sale"

    @api.multi
    def seacorp_print_receipt(self):
        datas = {'ids': self._ids,
                 'form': self.read()[0],
                 'model': 'pos.sale.report'
                 }
        docs = self.env['pos.session'].browse(self.session_id)
        print(self.session_id.order_ids)
        self.session_id.total_before_discount = 0
        self.session_id.total_discount = 0
        self.session_id.amount_total = 0
        for order in self.session_id.order_ids:
            # discount = 0
            order.total_discount = 0
            order.total_before_discount = 0
            for line in order.lines:
                order.total_before_discount += line.price_unit * line.qty
                order.total_discount += ((line.discount / 100) * line.price_unit * line.qty)

            self.session_id.total_before_discount += order.total_before_discount
            self.session_id.total_discount += order.total_discount
            self.session_id.amount_total += order.amount_total
        return self.env.ref('seacorp_pos_retail_report_pdf.seacorp_report_pos_sales_pdf').report_action(self.session_id)

    session_id = fields.Many2one('pos.session', string="Closed Session(s)")
    report_type = fields.Selection([('thermal', 'Thermal'),
                                    ('pdf', 'PDF')], default='pdf', readonly=True, string="Report Type")


class pos_session(models.Model):
    _inherit = "pos.session"

    total_before_discount = fields.Float()
    total_discount = fields.Float()
    amount_total = fields.Float()

class PosOrder(models.Model):
    _inherit = "pos.order"

    total_before_discount = fields.Float()
    total_discount = fields.Float()
