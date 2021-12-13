# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class AcsChangeReq(models.Model):
    _description = 'Change Request'
    _name = 'acs.change.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Subject', required=True, readonly=True, states={'draft': [('readonly', False)]})
    number = fields.Char(string='Number', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('approve', 'Approved'),
        ('disapprove', 'Disapproved'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', copy=False, default='draft', readonly=True, states={'draft': [('readonly', False)]}, track_visibility='onchange')
    date = fields.Date("Date", readonly=True, states={'draft': [('readonly', False)]}, default=fields.Date.today)
    description = fields.Text('Description', readonly=True, states={'draft': [('readonly', False)]})
    project_id = fields.Many2one('project.project', 'Project', ondelete='restrict', readonly=True, states={'draft': [('readonly', False)]})
    partner_id = fields.Many2one('res.partner', string='Customer', required=True, readonly=True, states={'draft': [('readonly', False)]})
    task_id = fields.Many2one('project.task', string='Task', readonly=True, states={'draft': [('readonly', False)]})
    user_id = fields.Many2one('res.users', string='User', readonly=True, states={'draft': [('readonly', False)]}, default=lambda self: self.env.user.id)

    @api.model
    def create(self, values):
        values['number'] = self.env['ir.sequence'].next_by_code('acs.change.request') or '/'
        return super(AcsChangeReq, self).create(values)

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.state not in ('draft', 'cancel'):
                raise UserError(_('You cannot delete an record which is not draft or cancelled.'))
        return super(AcsChangeReq, self).unlink()

    @api.multi
    def confirm_change_request(self):
        self.state = 'confirm'

    @api.multi
    def done_change_request(self):
        self.state = 'done'

    @api.multi
    def approve_change_request(self):
        self.state = 'approve'

    @api.multi
    def disapprove_change_request(self):
        self.state = 'disapprove'

    @api.multi
    def draft_change_request(self):
        self.state = 'draft'

    @api.multi
    def cancel_change_request(self):
        self.state = 'cancel'

    @api.onchange('task_id')
    def onchange_task(self):
        if self.task_id and self.task_id.project_id:
            self.project_id = self.task_id.project_id.id

    @api.onchange('project_id')
    def onchange_project(self):
        res = {'domain': {}}
        if self.project_id:
            self.task_id = False
            res['domain'].update({'task_id': [('project_id', '=', self.project_id.id)]})
        else:
            res['domain'].update({'task_id': []})
        return res

    @api.multi
    def action_create_task(self):
        Task = self.env['project.task']
        task = Task.create({
            'name': self.name,
            'partner_id': self.partner_id.id,
            'project_id': self.project_id and self.project_id.id or False,
            'user_id': self.user_id and self.user_id.id or False,
        })
        self.task_id = task.id

    @api.multi
    def change_request_task_action(self):
        return {
            'name': _('Task'),
            'view_type': 'form',
            'view_mode': 'kanban,tree,form,calendar,pivot,graph',
            'res_model': 'project.task',
            'type': 'ir.actions.act_window',
            'domain': [('id','in', self.task_id)],
            'context': {
            }
        }

    @api.multi
    def get_access_action(self):
        """ Override method that generated the link to access the change req. Instead
        of the classic form view, redirect to the post on the website directly"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': '/my/cangereq/%s' % self.id,
            'target': 'self',
            'res_id': self.id,
        }

    @api.multi
    def get_base_url(self):
        web_base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        return web_base_url


class ProjectProject(models.Model):
    _inherit = 'project.project'

    @api.multi
    def _chnage_req_count(self):
        for rec in self: 
            rec.chnage_req_count = len(rec.chnage_req_ids)

    chnage_req_count = fields.Integer(compute="_chnage_req_count", readonly=True, string="Change Requests")
    chnage_req_ids = fields.One2many('acs.change.request', 'project_id', string='Project Change Requests')

    @api.multi
    def project_chnage_req_action(self):
        return {
            'name': _('Change Requests'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'acs.change.request',
            'type': 'ir.actions.act_window',
            'domain': [('id','in', self.chnage_req_ids.ids)],
            'context': {
                'default_partner_id': self.partner_id.id,
                'default_project_id': self.id,
            }
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: