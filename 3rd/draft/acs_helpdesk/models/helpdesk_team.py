# -*- coding: utf-8 -*-

from odoo import fields, models, api, SUPERUSER_ID, _
from datetime import datetime, timedelta, date
from odoo.tools.safe_eval import safe_eval


class SupportTeam(models.Model):
    _name = 'support.team'
    _order = 'sequence asc'
    _description = 'Support Teams'

    @api.depends('percentage_satisfaction_ticket')
    def _compute_percentage_satisfaction_team(self):
        domain = [('create_date', '>=', fields.Datetime.to_string(fields.datetime.now() - timedelta(days=30)))]
        for team in self:
            activity = team.ticket_ids.rating_get_grades(domain)
            team.percentage_satisfaction_team = activity['great'] * 100 / sum(activity.values()) if sum(activity.values()) else -1

    @api.one
    @api.depends('ticket_ids.rating_ids.rating')
    def _compute_percentage_satisfaction_ticket(self):
        activity = self.ticket_ids.rating_get_grades()
        self.percentage_satisfaction_ticket = activity['great'] * 100 / sum(activity.values()) if sum(activity.values()) else -1

    percentage_satisfaction_ticket = fields.Integer(
        compute='_compute_percentage_satisfaction_ticket', string="Happy % on Task", store=True, default=-1)
    percentage_satisfaction_team = fields.Integer(
        compute="_compute_percentage_satisfaction_team", string="Happy % on Project", store=True, default=-1)

    name = fields.Char(required=True)
    sequence = fields.Integer(string='Sequence', index=True, default=10)
    member_ids = fields.Many2many('res.users', 'support_team_user_rel',
        'team_id', 'user_id', 'Support Team Members')
    color = fields.Integer("Color Index", default=0)
    ticket_ids = fields.One2many('acs.support.ticket', 'team_id', copy=False)

    # For the dashboard only
    todo_ticket_ids = fields.One2many('acs.support.ticket', string="Tickets", copy=False, compute='_compute_todo_tickets')
    todo_ticket_count = fields.Integer(string="Number of Tickets", compute='_compute_todo_tickets')
    todo_ticket_count_date = fields.Integer(string="Number of Tickets Scheduled", compute='_compute_todo_tickets')
    todo_ticket_count_high_priority = fields.Integer(string="Number of Tickets in High Priority", compute='_compute_todo_tickets')
    todo_ticket_count_block = fields.Integer(string="Number of Tickets Blocked", compute='_compute_todo_tickets')
    todo_ticket_count_unscheduled = fields.Integer(string="Number of Tickets Unscheduled", compute='_compute_todo_tickets')

    @api.one
    @api.depends('ticket_ids.stage_id')
    def _compute_todo_tickets(self):
        self.todo_ticket_ids = self.ticket_ids.filtered(lambda e: e.stage_id.done==False)
        self.todo_ticket_count = len(self.todo_ticket_ids)
        self.todo_ticket_count_date = len(self.todo_ticket_ids.filtered(lambda e: e.schedule_date != False))
        self.todo_ticket_count_high_priority = len(self.todo_ticket_ids.filtered(lambda e: e.priority == '3'))
        self.todo_ticket_count_block = len(self.todo_ticket_ids.filtered(lambda e: e.kanban_state == 'blocked'))
        self.todo_ticket_count_unscheduled = len(self.todo_ticket_ids.filtered(lambda e: not e.schedule_date))

    @api.multi
    def action_view_all_rating(self):
        """ return the action to see all the rating of the project, and activate default filters """
        action = self.env['ir.actions.act_window'].for_xml_id('acs_helpdesk', 'rating_rating_action_view_team_rating')
        action['name'] = _('Ratings of %s') % (self.name,)
        action_context = safe_eval(action['context']) if action['context'] else {}
        action_context.update(self._context)
        action_context['search_default_rating_tasks'] = 1
        return dict(action, context=action_context)


