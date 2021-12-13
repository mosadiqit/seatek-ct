# Copyright 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields

class SeaEmployeeEducationLevel(models.Model):

    _name = 'hr.employee.education_level'
    _description = 'Employee Education Level'
    name = fields.Char(string='Employee Education', translate=True)



class HrEmployee(models.Model):
    """Added academic, certification and experience details for employee."""

    _inherit = 'hr.employee'

    academic_ids = fields.One2many('hr.academic',
                                   'employee_id',
                                   'Academic Experiences',
                                   help="Academic Experiences")
    certification_ids = fields.One2many('hr.certification',
                                        'employee_id',
                                        'Certifications',
                                        help="Certifications")
    experience_ids = fields.One2many('hr.experience',
                                     'employee_id',
                                     ' Professional Experiences',
                                     help='Professional Experiences')
    sea_certificate_level = fields.Selection([
        ('master', 'Master'),
        ('bachelor', 'Bachelor'),
        ('college', 'College'),
        ('intermediate', 'Intermediate'),
        ('general ', 'General'),
        ('diploma', 'Diploma/Certificate'),
        ('other', 'Other'),
    ], 'Degree Level', default='other', groups="hr.group_hr_user")

    employee_education_level = fields.Many2one('hr.employee.education_level', string="Education Level")
