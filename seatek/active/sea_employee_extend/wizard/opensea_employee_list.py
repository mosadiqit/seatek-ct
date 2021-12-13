from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval
from odoo.tools import pycompat
from odoo.fields import Datetime


class OpenseaEmployeeListWizard(models.TransientModel):
    _name = 'opensea.employee.list.wizard'
    _description = 'Opensea Employee List Wizard'

    company_ids = fields.Many2many(
        'res.company', default=lambda self: self.env.user.company_id
    )

    @api.multi
    def find_objs(self):
        if self.company_ids:
            if len(self.company_ids) == 1:
                objs_search = self.env['hr.employee'].search([('company_id', '=', self.company_ids.id)])
            if len(self.company_ids) == 2:
                objs_search = self.env['hr.employee'].search([('company_id', 'in', self.company_ids.ids)])
        if not objs_search:
            raise ValidationError(_('The period choose has no data to report! Please select a different time period.'))
        else:
            return objs_search

    @api.multi
    def export_employee_list(self):
        self.ensure_one()
        if not self.env.user.tz:
            raise ValidationError(_('Please contact Administrator to configure your time zone!!!'))
        else:
            data = self.read()[0]
            objs_list_employee = self.find_objs()
            datas = {
                'ids': objs_list_employee.ids,
                # 'model': 'hr.employee',
                # 'form': data,
                # 'product': self.product_ids.ids,
                # 'location': self.location_ids.ids,
                # 'picking_type': self.picking_type_ids.ids,
            }
            return self.env['ir.actions.report'].search(
                [('report_name', '=', 'sea_employee_extend.employee_list_report_xls'),
                ('report_type', '=', 'xlsx')],
                limit=1).report_action(self, data=datas)
