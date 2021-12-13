# -*- coding: utf-8 -*-

from odoo import fields, models, api, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta, date
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class TicketStage(models.Model):
    _name = 'acs.support.stage'
    _order = 'sequence asc'
    _description = "Website Support Stage"

    name = fields.Char(string="Name")
    sequence = fields.Integer(string='Sequence', index=True, default=10)
    team_ids = fields.Many2many('support.team', 'support_team_stage_rel',
        'team_id', 'stage_id', 'Support Teams')
    done = fields.Boolean('Done')
    fold = fields.Boolean('Folded in Kanban')
    email_template_id = fields.Many2one('mail.template', domain="[('model','=','acs.support.ticket')]", string="Notification Email Template")
    rating_template_id = fields.Many2one('mail.template', string='Rating Email Template',
        domain=[('model', '=', 'acs.support.ticket')],
        help="If set and if the Team's rating configuration is 'Rating when changing stage', then an email will be sent to the customer when the ticket reaches this step.")


class WebsiteSupportTicket(models.Model):
    _name = "acs.support.ticket"
    _description = "Website Support Ticket"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin', 'rating.mixin']
    _mail_post_access = 'read'
    _order = 'sequence asc'

    def _get_default_stage_id(self):
        """ Gives default stage_id """
        team_id = self.env.context.get('default_team_id')
        if not team_id:
            return False
        return self.stage_find(team_id, [('fold', '=', False)])

    def _get_default_project_id(self):
        project_id = self.env.user.sudo().company_id.support_project_id and self.env.user.sudo().company_id.support_project_id.id or False
        return project_id
 
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        search_domain = [('id', 'in', stages.ids)]
        if 'default_team_id' in self.env.context:
            search_domain = ['|', ('team_ids', '=', self.env.context['default_team_id'])] + search_domain

        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    def _time_count(self):
        for rec in self:
            if rec.date_start and not rec.start_stop:
                datetime_diff = datetime.now() - datetime.strptime(rec.date_start, DEFAULT_SERVER_DATETIME_FORMAT)
                hrs = datetime_diff.seconds / 3600
                mins = datetime_diff.seconds % 3600 / 60
                rec.time_count = "%s:%s" % (hrs, mins)
            else:
                rec.time_count = "0.0"

    @api.depends('stage_id', 'timesheet_ids.unit_amount')
    def _hours_get(self):
        for task in self:
            task.total_hours_spent = sum(task.sudo().timesheet_ids.mapped('unit_amount'))  # use 'sudo' here to allow project user (without timesheet user right) to create task

    number = fields.Char(string="Ticket Number")
    tag_ids = fields.Many2many('helpdesk.tags', string='Tags')
    schedule_date = fields.Date(string='Sheduled Date', index=True, copy=False)
    date_deadline = fields.Date(string='Deadline', index=True, copy=False)
    team_id = fields.Many2one('support.team', "Support Team")

    date_start = fields.Datetime('Start Time')
    date_end = fields.Datetime('Stop Time')
    start_stop = fields.Boolean(string='Start Stop', default=False)
    time_count = fields.Char(compute="_time_count", string="Working Time")
    running_work_description = fields.Char(string="Work Description")

    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Priority')
    sequence = fields.Integer(string='Sequence', index=True, default=10,
        help="Gives the sequence order when displaying a list of tasks.")
    stage_id = fields.Many2one('acs.support.stage', string='Stage', track_visibility='onchange', index=True,
        default=_get_default_stage_id, group_expand='_read_group_stage_ids',
        domain="[('team_ids', '=', team_id)]", copy=False)
    kanban_state = fields.Selection([('normal', 'In Progress'), ('blocked', 'Blocked'), ('done', 'Ready for next stage')],
                                    string='Kanban State', required=True, default='normal', track_visibility='onchange')

    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    user_id = fields.Many2one('res.users', string="Assigned User")
    email = fields.Char(string="Email")
    category_id = fields.Many2one('acs.support.ticket.categories', string="Category", track_visibility='onchange')
    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    color = fields.Char(string="Ticket Color")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env['res.company']._company_default_get('acs.support.ticket') )
    close_date = fields.Date(string="Close Date")

    timesheet_ids = fields.One2many('account.analytic.line', 'ticket_id', string="Timesheet")
    project_id = fields.Many2one('project.project', string="Timesheet Project",
        default=_get_default_project_id,)
    invoice_type = fields.Selection([
        ('no', 'No Invoice'),
        ('normal', 'Normal Cost'), 
        ('fix', 'Fix Cost'), 
        ('timesheet', 'Based on Timesheet')], 
        string='Invoice Policy', default='normal', required=True)
    timesheet_invoice_product_id = fields.Many2one('product.product', string='Timesheet Invoice Product')
    invoice_product_id = fields.Many2one('product.product', string='Invoice Product')
    invoice_id = fields.Many2one('account.invoice', 'Invoice', ondelete="cascade", copy=False)
    support_price = fields.Float('Support Price')
    total_hours_spent = fields.Float(compute='_hours_get', store=True, string='Total Hours', help="Computed as: Time Spent Hours.")

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.email = self.partner_id.email

    @api.onchange('team_id')
    def _onchange_project(self):
        if self.team_id and self.team_id not in self.stage_id.team_ids:
                self.stage_id = self.stage_find(self.team_id.id, [('fold', '=', False)])
        else:
            self.stage_id = False

    # ----------------------------------------
    # Case management
    # ----------------------------------------

    def stage_find(self, section_id, domain=[], order='sequence'):
        """ Override of the base.stage method
            Parameter of the stage search taken from the lead:
            - section_id: if set, stages must belong to this section or
              be a default stage; if not set, stages must be default
              stages
        """
        # collect all section_ids
        section_ids = []
        if section_id:
            section_ids.append(section_id)
        section_ids.extend(self.mapped('team_id').ids)
        search_domain = []
        if section_ids:
            search_domain = [('|')] * (len(section_ids) - 1)
            for section_id in section_ids:
                search_domain.append(('team_ids', '=', section_id))
        search_domain += list(domain)
        # perform search, return the first found
        return self.env['acs.support.stage'].search(search_domain, order=order, limit=1).id

    @api.multi
    def action_start(self):
        action_click = self.search_count([('start_stop','=',True),('user_id', '=',self.env.uid)])
        if action_click >= 1:
            raise UserError(_('You cannot start multiple Ticket. Another Ticket is already in progress.'))
        else:
            ms = _("Started by %s.") % (self.env.user.name)
            self.message_post(body=ms)
            return self.write({'date_start': datetime.now(), 'date_end': False, 'start_stop': True, 'running_work_description': self.name})

    @api.multi
    def action_stop(self):
        datetime_diff = datetime.now() - self.date_start
        m, s = divmod(datetime_diff.total_seconds(), 60)
        h, m = divmod(m, 60)
        dur_h = (_('%0*d')%(2,h))
        dur_m = (_('%0*d')%(2,m*1.677966102))
        duration = dur_h+'.'+dur_m

        project_id = self.project_id or self.env.user.company_id.support_project_id
        if not project_id:
            raise UserError(_('Please set project on ticket or Configure project first in configuration.'))

        if not self.running_work_description:
            raise UserError(_('Please enter work description before stopping task.'))
        self.write({
            'start_stop': False,
            'date_end': datetime.now(),
            'running_work_description': '',
            'date_start': False,
            'timesheet_ids': [(0, 0, {
                'name': self.running_work_description,
                'account_id': project_id.analytic_account_id.id,
                'unit_amount': float(duration),
                'company_id': self.env.user.company_id.id,
                'user_id': self.env.user.id,
                'date_start': self.date_start,
                'date_stop': datetime.now(),
                'project_id': project_id.id,
                'ticket_id': self.id,
             })]
        })
        ms = _("Stopped by %s.") % (self.env.user.name)
        self.message_post(body=ms) 
        return True

    @api.multi
    def create_invoice(self):
        inv_obj = self.env['account.invoice']
        ir_property_obj = self.env['ir.property']
        inv_line_obj = self.env['account.invoice.line']
        account_id = product_id = False
        if self.invoice_type in ['normal','fix']:
            product_id = self.invoice_product_id or self.company_id.support_invoice_product_id

        if self.invoice_type=='timesheet':
            product_id = self.timesheet_invoice_product_id or self.company_id.support_timesheet_invoice_product_id

        if not product_id:
            raise UserError(_('Please configure Helpdesk Invoice Product on Configuration.'))

        if product_id.property_account_income_id:
            account_id = product_id.property_account_income_id.id
        elif product_id.categ_id.property_account_income_categ_id:
            account_id = product_id.categ_id.property_account_income_categ_id.id
        else:
            prop = ir_property_obj.get('property_account_income_categ_id', 'product.category')
            account_id = prop and prop.id or False
        if not account_id:
            raise UserError(_('Please configure proper accounts on Helpdesk Invoice Product on Configuration.'))

        amount = 0
        quantity = 1
        if self.invoice_type=='normal':
            amount = product_id.lst_price
        elif self.invoice_type=='fix':
            amount = self.support_price
        elif self.invoice_type=='timesheet':
            amount = product_id.lst_price
            quantity = self.total_hours_spent

        invoice = inv_obj.create({
            'account_id': self.partner_id.property_account_receivable_id.id,
            'partner_id': self.partner_id.id,
            'type': 'out_invoice',
            'origin': self.name,
            'invoice_line_ids': [(0, 0, {
                'name': product_id.name,
                'price_unit': amount,
                'account_id': account_id,
                'quantity': quantity,
                'discount': 0.0,
                'uom_id': product_id.uom_id.id,
                'product_id': product_id.id,
                'account_analytic_id': False,
            })],
        })
        self.state = 'done'
        self.invoice_id = invoice.id

    @api.model
    def create(self, vals):
        vals['number'] = self.env['ir.sequence'].next_by_code('acs.support.ticket') or '/'
        rec = super(WebsiteSupportTicket, self).create(vals)
        new_ticket_template = self.env['ir.model.data'].get_object('acs_helpdesk', 'support_ticket_new')
        new_ticket_template.send_mail(rec.id, True)
        return rec

    @api.multi
    def write(self, values, context=None):
        res = super(WebsiteSupportTicket, self).write(values)
        if 'stage_id' in values and values.get('stage_id'):
            self._send_ticket_rating_mail(force_send=True)
            self._send_ticket_notification_mail(force_send=True)
        return res

    def _send_ticket_notification_mail(self, force_send=False):
        for ticket in self:
            email_template_id = ticket.stage_id.email_template_id
            if email_template_id:
                email_template_id.send_mail(ticket.id, True)

    def _send_ticket_rating_mail(self, force_send=False):
        for ticket in self:
            rating_template = ticket.stage_id.rating_template_id
            if rating_template:
                ticket.rating_send_request(rating_template, lang=ticket.partner_id.lang, force_send=force_send)

    def rating_get_parent(self):
        return 'team_id'


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    date_start = fields.Datetime('Start Time')
    date_stop = fields.Datetime('End Time')
    ticket_id = fields.Many2one('acs.support.ticket', string="Support Ticket")


class WebsiteSupportTicketCategories(models.Model):
    _name = "acs.support.ticket.categories"
    _description = "Support Category"
    _order = "sequence asc"

    sequence = fields.Integer(string="Sequence")
    name = fields.Char(required=True, translate=True, string='Category Name')


class HelpdeskTags(models.Model):
    """ Tags of helpdesk's Tickets """
    _name = "helpdesk.tags"
    _description = "Tags of project's tasks"

    name = fields.Char(required=True)
    color = fields.Integer(string='Color Index', default=10)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]