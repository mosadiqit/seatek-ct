# -*- coding: utf-8 -*-
# Part of OpenSea12 , last modified 12/03/2020 by htkhoa
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
class ContractPeriod(models.Model):

    _name = 'hr.contract.period'
    _description = 'Contract Period'
    _order = 'sequence, id'

    name = fields.Char(string='Contract Period', required=True, translate=True)
    sequence = fields.Integer(help="Gives the sequence when displaying a list of Contract Period.", default=10)

class SeaExtendContract(models.Model):
    _inherit = "hr.contract"
    _description = 'Sea Extend Contract'

    contract_category = fields.Selection([('contract', 'Contract'),
                                 ('addition', 'Addition')], string='Category', help='Contract Category')
    ref_contract_id = fields.Many2one('hr.contract', string='Ref Contract')
    contract_period_id = fields.Many2one('hr.contract.period', string="Contract Period", required=True, default=lambda self: self.env['hr.contract.period'].search([], limit=1))
    contract_term= fields.Text(string='Contract Term')
    contract_extend_salary = fields.Monetary('Extend Salary', digits=(16, 2), required=False, track_visibility="onchange", help="Employee's monthly Extend Salary.")

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            self.ref_contract_id = False
            return {'domain': {'ref_contract_id': [('employee_id', '=', self.employee_id.id)]}}
        else:
            # remove the domain
            return {'domain': {'ref_contract_id': []}}