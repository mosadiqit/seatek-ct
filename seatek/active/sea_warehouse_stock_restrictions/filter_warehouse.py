# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import Warning


class FilterWarehouse(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def get_restrict_warehouse(self):
        if 'warehouse_ids' in self.env.user:
            res = []
            for item in self.env.user.warehouse_ids:
                res.append(item.id)
            return res

    warehouse_id = fields.Many2one(
        'stock.warehouse', string='Warehouse',
        required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        domain=lambda self: [('id', 'in', self.get_restrict_warehouse())])
