# -*- coding: utf-8 -*-
from openerp import api, fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"

    def _count_support_tickets(self):
        for rec in self:
            rec.ticket_count = len(rec.ticket_ids.ids)

    ticket_ids = fields.One2many('acs.support.ticket', 'partner_id', string='Tickets')
    ticket_count = fields.Integer(compute="_count_support_tickets", string="Ticket Count")
