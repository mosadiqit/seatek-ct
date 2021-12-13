from odoo import models, fields, api
from odoo.addons.global_seatek import Seatek

class AccountInvoice(models.Model, Seatek):
    _inherit = 'account.invoice'

    is_dannygreen_print = fields.Boolean('DannyGreen Print', default=False, compute='_is_dannygreen_print')
    total_discount = fields.Monetary(string='Amount discount', store=True, readonly=True,
                                     help="Total amount discount")

    # @api.depends('amount_total', 'total_discount')
    # def _total_discount(self):
    #     for p in self:
    #         total = 0
    #         for l in p.invoice_line_ids:
    #             total += l.price_discount
    #         p.total_discount = total

    @api.multi
    def _is_dannygreen_print(self):
        for s in self:
            s.is_dannygreen_print = s.env.user.company_id.dannygreen_account_form_report

    def dannygreen_report_selection(self):
        form_view_id = self.env.ref(
            'dannygreen_account_print_pdf.view_dannygreen_account_invoicing_selection_report').id
        action = {
            'name': 'DannyGreen Report',
            'res_model': 'dannygreen.account.report.selection',
            'type': 'ir.actions.act_window',
            'context': {},
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': form_view_id,
            'target': 'new'
        }
        return action

    @api.model
    def format_date(self):
        if self.date_invoice:
            return self.date_invoice.strftime("Ngày %d tháng %m năm %Y")
        return ""

    @api.model
    def get_user_changed_ready(self):
        return self.get_user_changed_stt('ready')

    @api.model
    def get_user_changed_done(self):
        return self.get_user_changed_stt('done')

    @api.model
    def get_user_changed_stt(self, stt=None):
        messages = self.env['mail.message'].search([('res_id', '=', self.id)])
        mail_tracking_values = self.env['mail.tracking.value'].search([('mail_message_id', 'in', messages.ids)])
        for v in mail_tracking_values:
            new_stt = str(v.new_value_char).lower()
            if new_stt == stt:
                if v.mail_message_id.author_id:
                    return v.mail_message_id.author_id.name
        return ""

    @api.model
    def get_sale_order(self):
        sale_line_ids = self.invoice_line_ids.mapped('sale_line_ids')
        if sale_line_ids:
            sale_order = sale_line_ids[0].order_id
            return sale_order
        return False

    @api.model
    def get_warehouse(self):
        sale_order = self.get_sale_order()
        if sale_order:
            if sale_order.warehouse_id:
                return sale_order.warehouse_id.name
        return ""


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    price_discount = fields.Monetary(string='Amount discount',
                                     store=True, readonly=True,
                                     help="Total amount discount")
    price_total_without_discount = fields.Monetary(string='Amount without discount',
                                                   store=True, readonly=True,
                                                   help="Total amount discount")

    # @api.depends('price_total', 'price_total_without_discount', 'price_discount', 'discount')
    # def _get_price_discount(self):
    #     total = self.price_total * 100 / (100 - self.discount)
    #     self.price_discount = total - self.price_total
    #     self.price_total_without_discount = total
