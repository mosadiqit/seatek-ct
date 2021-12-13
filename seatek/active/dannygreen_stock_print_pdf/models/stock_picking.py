from odoo import models, fields, api
from odoo.addons.global_seatek import Seatek


class Picking(models.Model, Seatek):
    _inherit = 'stock.picking'

    is_dannygreen_print = fields.Boolean('DannyGreen Print', default=False, compute='_is_dannygreen_print')
    amount_total = fields.Float(string='Amount total', store=True, readonly=True, track_visibility='always')

    @api.multi
    def _is_dannygreen_print(self):
        for s in self:
            s.is_dannygreen_print = s.env.user.company_id.dannygreen_stock_form_report

    def dannygreen_report_selection(self):
        form_view_id = self.env.ref('dannygreen_stock_print_pdf.view_stock_selection_report').id
        action = {
            'name': 'DannyGreen Report',
            'res_model': 'stock.report.selection',
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
        if self.scheduled_date:
            return self.scheduled_date.strftime("Ngày %d tháng %m năm %Y")
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


class StockMove(models.Model):
    _inherit = 'stock.move'

    price_total = fields.Float(string='Price total', store=True, readonly=True)
    # price_unit_with_tax = fields.Float()
