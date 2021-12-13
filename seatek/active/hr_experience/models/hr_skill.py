# Copyright 2013 Savoir-faire Linux
# Copyright 2018-2019 Brainbean Apps
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class Skill(models.Model):
    _name = 'hr.skill'
    _description = 'HR Skill'
    _parent_store = True
    _order = 'complete_name'
    _rec_name = 'complete_name'

    name = fields.Char(
        string='Name',
        required=True,
        translate=True,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    parent_id = fields.Many2one(
        string='Parent',
        comodel_name='hr.skill',
        ondelete='cascade',
    )
    parent_path = fields.Char(
        index=True,
    )
    complete_name = fields.Char(
        string='Complete Name',
        compute='_compute_complete_name',
        store=True,
    )
    child_ids = fields.One2many(
        string='Children',
        comodel_name='hr.skill',
        inverse_name='parent_id',
    )
    employee_skill_ids = fields.One2many(
        string='Employees',
        comodel_name='hr.employee.skill',
        inverse_name='skill_id',
    )
    description = fields.Char(
        string='Description'
    )
    color = fields.Integer(
        string='Color Index',
        default=10,
    )

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for group in self:
            if group.parent_id:
                group.complete_name = _('%(parent)s / %(own)s') % ({
                    'parent': group.parent_id.complete_name,
                    'own': group.name,
                })
            else:
                group.complete_name = group.name

class EmployeeSkill(models.Model):
    _name = 'hr.employee.skill'
    _description = 'HR Employee Skill'
    _rec_name = 'complete_name'

    employee_id = fields.Many2one(
        string='Employee',
        comodel_name='hr.employee',
    )
    skill_id = fields.Many2one(
        string='Skill',
        comodel_name='hr.skill',
    )
    level = fields.Selection(
        string='Level',
        selection=[
            ('0', 'Junior'),
            ('1', 'Intermediate'),
            ('2', 'Senior'),
            ('3', 'Expert'),
        ],
    )
    complete_name = fields.Char(
        string='Complete Name',
        compute='_compute_complete_name',
        store=True,
    )

    _sql_constraints = [
        (
            'hr_employee_skill_uniq',
            'unique(employee_id, skill_id)',
            'This employee already has that skill!'
        ),
    ]

    @api.multi
    @api.depends('employee_id.name', 'skill_id.name', 'level')
    def _compute_complete_name(self):
        levels = dict(self._fields['level'].selection)
        for employee_skill in self:
            employee_skill.complete_name = _(
                '%(employee)s, %(skill)s (%(level)s)'
            ) % {
                'employee': employee_skill.employee_id.name,
                'skill': employee_skill.skill_id.name,
                'level': levels.get(employee_skill.level),
            }

class Employee(models.Model):
    _inherit = 'hr.employee'

    employee_skill_ids = fields.One2many(
        string='Skills',
        comodel_name='hr.employee.skill',
        inverse_name='employee_id',
    )
