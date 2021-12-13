# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    state_last_work_order = fields.Char(string='Current Work Order', default='', compute='_compute_state')

    @api.depends('state_last_work_order')
    def _compute_state(self):
        for record in self:
            workOrders = []
            for wo in record.workorder_ids:
                if wo.state == 'progress':
                    workOrders.append(wo)
            if len(workOrders) > 0:
                workOrders.sort(key=lambda x: x.id)
                record.state_last_work_order = workOrders[len(workOrders) - 1].name