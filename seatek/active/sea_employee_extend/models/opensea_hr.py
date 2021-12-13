from datetime import datetime, timedelta
from odoo import fields, models

class EmployeeStatus(models.Model):

    _name = 'hr.employee.status'
    _description = 'Employee Status'
    name = fields.Char(string='Employee Status', translate=True)


class EmployeeLevel(models.Model):

    _name = 'hr.employee.level'
    _description = 'Employee Level'
    _order = 'level, id'

    level = fields.Integer(string='Level', required=True, help="Level", default=1, translate=True)
    name = fields.Char(string='Employee Level ', required=True, translate=True)

    _sql_constraints = [
        ('field_unique_level',
         'unique(level)',
         'Choose another value for level - it has to be unique!')
    ]



class HREmployee(models.Model):
    _inherit = "hr.employee"

    sc_code = fields.Char(
        string='Employee Code',
        groups = 'hr.group_hr_user',
    )

    sea_company_ids = fields.Many2many('res.company', string='Sea Companies')

#    identification_issue_date = fields.Date(string='Identification Issue Date')
#    identification_issue_office = fields.Text(string='Identification Issue Office')
#    passport_issue_date = fields.Date(string='Passport Issue Date')
#    passport_issue_office = fields.Text(string='Passport Issue Office')
 # Not used
#    home_town = fields.Text(string='Home Town')
    temporary_address = fields.Many2one('res.partner', 'Temporary Address', groups="hr.group_hr_user")

    seagroup_join_date = fields.Date(string='Seagroup Join Date')
    official_contract = fields.Date(string='Official Contract')
#    employee_status = fields.Many2one('hr.employee.status', string="Employee Status")
    employee_current_status = fields.Selection([
                                            ('working', 'Working'),
                                            ('leaving', 'Temporary Leaving'),
                                            ('resigned', 'Resigned')
                                       ], string='Employee Status', help='Employee Status')
    reason_leaving = fields.Text(string='Leaving Reason')
    resignation_date = fields.Date(string='Resignation Date')
    extra_note = fields.Text(string='Extra Note')

    # TNCN
    tax_tncn_code = fields.Char(string='Mã số thuế TNCN')
    number_of_dependents = fields.Char(string='Số người phụ thuộc')
    info_dependents = fields.Text(string='Info Dependents')

    # BHXH
    social_insurance_number = fields.Text(string='Social Insurance Number')
    insurance_status = fields.Text(string='Insurance Status')

    sea_bank_account = fields.Text(string='Bank Account')
    ethnicity = fields.Text(string='Ethnicity')
    religion = fields.Text(string='Religion')

    #Income Information
    sea_net_salary = fields.Float('Trial salary', digits=None,track_visibility="onchange", help="Trial Salary.")
    sea_contract_salary = fields.Float('Contract salary', digits=None, track_visibility="onchange",help="Net Salary.")
    sea_extend_salary = fields.Float('Extend salary', digits=None, track_visibility="onchange",help="Extend Salary.")

    sea_employee_level = fields.Many2one('hr.employee.level', string="Employee Level", required=True, default=lambda self: self.env['hr.employee.level'].search([], limit=1))

