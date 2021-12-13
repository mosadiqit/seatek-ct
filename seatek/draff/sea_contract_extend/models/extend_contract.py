from datetime import datetime, timedelta
from odoo import models, fields, _


class ExtendPrivateInformation(models.Model):
    _inherit = "hr.contract"
    _description = 'HR Extend Contract'

    contract_type = fields.Many2many('note.tag', string="Contract Type")
    contract_term= fields.Text(string='Contract Term')
