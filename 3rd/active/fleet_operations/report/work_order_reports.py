from odoo import models, fields, api, _


class WorkOrderReports(models.TransientModel):
    _name = 'work.order.reports'
    _description = "Work Order Reports"

    select_report = fields.Selection([('wo_month_sum_rep', 'Work Order Monthly Summary Report'),
                             ('wo_over_10_days', 'Work Order Over 10 Days'),
                             ('outstanding_wo', 'Outstanding Work Order'),
                             ('wo_summary', 'Work Order Summary'),
                             ('wo', 'Work Order')])
    name = fields.Char("Name", default = 'Genric Report.xls')
    vehicle_ids = fields.Many2many('fleet.vehicle', 'fleet_wo_report_rel',
                                   'wor_id', 'vehicle_id',
                                   string="Vehicle")
    file = fields.Binary("Click On Download Link To Download Xls File",
                         readonly = True)

    @api.multi
    def print_wo_xlsx_report(self):
        for vehicle in self:
            wo_obj = self.env['fleet.vehicle.log.services']
            records = wo_obj.search([])
            if vehicle.vehicle_ids:
                records = wo_obj.search([('vehicle_id', 'in', vehicle.vehicle_ids.ids)])
            if vehicle.select_report == 'wo_month_sum_rep':
                wo_mon_rep_obj = self.env['report.fleet_operations.workorder.monthly.summary.xls']
                file = wo_mon_rep_obj.generate_xlsx_report(records)
                vehicle.write({'name': 'WorkOrder Monthly Summary Report.xls',
                               'file': file})
            elif vehicle.select_report == 'wo_over_10_days':
                wo_over_10d_obj = self.env['report.fleet_operations.wo.over.daysxls']
                file = wo_over_10d_obj.generate_xlsx_report(records)
                vehicle.write({'name': 'WorkOrder Over 10 Days.xls',
                               'file': file})
            elif vehicle.select_report == 'outstanding_wo':
                outstanding_wo_obj = self.env['report.fleet_operations.outstanding.wo.xls']
                file = outstanding_wo_obj.generate_xlsx_report(records)
                vehicle.write({'name': 'Outstanding Work Order.xls',
                               'file': file})
            elif vehicle.select_report == 'wo_summary':
                wo_summary_obj = self.env['report.fleet_operations.workorder.summary.xls']
                file = wo_summary_obj.generate_xlsx_report(records)
                vehicle.write({'name': 'Work Order Summary.xls',
                               'file': file})
            elif vehicle.select_report == 'wo':
                wo_obj1 = self.env['report.fleet_operations.fleet.history.work.order.xls']
                file = wo_obj1.generate_xlsx_report(records)
                vehicle.write({'name': 'Work Order.xls',
                               'file': file})
            return {
                  'view_type': 'form',
                  'view_mode': 'form',
                  'res_model': 'work.order.reports',
                  'type': 'ir.actions.act_window',
                  'target': 'new',
                  'res_id': vehicle.id
                }