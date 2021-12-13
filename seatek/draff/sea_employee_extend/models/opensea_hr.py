from datetime import datetime, timedelta
from odoo import fields, models

class EmployeeStatus(models.Model):

    _name = 'hr.employee.status'
    _description = 'Employee Status'
    name = fields.Char(string='Employee Status', translate=True)

class HREmployee(models.Model):
    _inherit = "hr.employee"

    sc_code = fields.Char(
        string='Employee Code',
        groups = 'hr.group_hr_user',
    )
    identification_issue_date = fields.Date(string='Identification Issue Date')
    identification_issue_office = fields.Text(string='Identification Issue Office')
    passport_issue_date = fields.Date(string='Passport Issue Date')
    passport_issue_office = fields.Text(string='Passport Issue Office')
    home_town = fields.Text(string='Home Town')

    temporary_address = fields.Many2one('res.partner', 'Temporary Address', groups="hr.group_hr_user")

    ethnicity = fields.Text(string='Ethnicity')
    religion = fields.Text(string='Religion')

    seagroup_join_date = fields.Date(string='Seagroup Join Date')
    official_contract = fields.Date(string='Official Contract')
    employee_status = fields.Many2one('hr.employee.status', string="Employee Status")
    reason_leaving = fields.Text(string='Reason Leaving')
    resignation_date = fields.Date(string='Resignation Date')
    extra_note = fields.Text(string='Extra Note')

    # TNCN
    tax_tncn_code = fields.Char(string='Mã số thuế TNCN')
    number_of_dependents = fields.Char(string='Số người phụ thuộc')
    info_dependents = fields.Text(string='Info Dependents')

    # BHXH
    social_insurance_number = fields.Text(string='Social Insurance Number')
    insurance_status = fields.Text(string='Insurance Status')
    bank_account = fields.Text(string='Bank Account')