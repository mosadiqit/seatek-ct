# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PosConfigReport(models.Model):
    _inherit = ['pos.config']

    @api.multi
    def action_report_session(self):
        action = self.env.ref('sea_report_xls.report_xls_pos_session_wizard_form', False)
        wiz = self.env['sea_report_xls.pos_session_wizard'].create({'name': self.name})
        wiz.pos_config = self
        return {
            'name': _('Report Session'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sea_report_xls.pos_session_wizard',
            'view_id': action.id,
            'target': 'new',
            'res_id': wiz.id,
            'context': self.env.context,
        }

class WizardReportPosSession(models.TransientModel):
    _name = 'sea_report_xls.pos_session_wizard'

    date_from = fields.Datetime(string='Date From', default=fields.Datetime.now)
    date_to = fields.Datetime(string='Date To', default=fields.Datetime.now)
    pos_config = fields.Many2one('pos.config',string='POS Name', copy=False)
    session_id = fields.Many2one('pos.session', string='Session Name')
    session_name = fields.Char(related='pos_config.session_ids.name',string='Current Session')
    report_type = fields.Selection([('xlsx', 'Excel'), ('csv', 'CSV')], string='Report Type', default='xlsx')
    type = fields.Selection([('current', 'Current Session'),
                ('session', 'By Session'),
                ('time', 'By Date'),
                ('user', 'By User'),], string='Type', default='current')

    @api.constrains('date_from', 'date_to')
    def _constrain_dates(self):
        for rec in self:
            if rec.date_from > rec.date_to:
                raise ValidationError(_('Date From must be greater than date To!'))

    @api.multi
    def find_session(self, session):
        session_obj = self.env['pos.session']
        session_search = session_obj.search([('name', '=', session)])
        if session_search:
            return session_search
        else:
            raise Warning(_(' "%s" Session is not available.') % session_name)

    @api.multi
    def view_report(self):
        if not self.session_id:
            self.session_id = self.find_session(self.session_name)
        data = self.read()[0]
        datas = {
            'ids': [],
            'model': 'sea_report_xls.pos_session_xls',
            'form': data
        }
        if self.report_type == 'xlsx':
            report = self.env['ir.actions.report'].search(
                [('report_name', '=', 'sea_report_xls.pos_session_xls'),
                ('report_type', '=', 'xlsx')],
                limit=1).report_action(self, datas)
        elif self.report_type == 'csv':
            report = self.env['ir.actions.report'].search(
                [('report_name', '=', 'sea_report_xls.pos_session_csv'),
                ('report_type', '=', 'csv')],
                limit=1).report_action(self, datas)
        else:
            report = self.env['ir.actions.report'].search(
                [('report_name', '=', 'sea_report_xls.pos_session_xls'),
                ('report_type', '=', 'xlsx')],
                limit=1).report_action(self, datas)
        return report
