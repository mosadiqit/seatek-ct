from datetime import datetime, timedelta
from odoo import models, fields, _


class ExtendPrivateInformation(models.Model):
    _inherit = "hr.employee"
    _description = 'HR Extend Private Information'

    identification_issue_date = fields.Date(string='Identification Issue Date')
    identification_issue_office = fields.Text(string='Identification Issue Office')
    passport_issue_date = fields.Date(string='Passport Issue Date')
    passport_issue_office = fields.Text(string='Passport Issue Office')
    home_town = fields.Text(string='Home Town')

    temporary_address = fields.Many2one('res.partner', 'Temporary Address', groups="hr.group_hr_user")

    ethnicity = fields.Text(string='Ethnicity')
    religion = fields.Text(string='Religion')