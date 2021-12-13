# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import Warning
from odoo.addons.purchase.models.purchase import PurchaseOrder as Purchase


class FilterWarehousePickingType(models.Model):
    _inherit = 'stock.picking.type'

    @api.multi
    def get_restrict_warehouse(self):
        if 'warehouse_ids' in self.env.user:
            res = []
            for item in self.env.user.warehouse_ids:
                res.append(item.id)
            return res

    warehouse_id = fields.Many2one(
        'stock.warehouse', string='Warehouse', ondelete='cascade',
        domain=lambda self: [('id', 'in', self.get_restrict_warehouse())])


class FilterPurchasPickingType(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def get_restrict_warehouse(self):
        if 'warehouse_ids' in self.env.user:
            res = []
            for item in self.env.user.warehouse_ids:
                res.append(item.id)
            print(res)
            return res

    @api.multi
    def get_restrict_picking_type(self):
        if 'default_picking_type_ids' in self.env.user:
            res = []
            for item in self.env.user.default_picking_type_ids:
                res.append(item.id)
            print(res)
            return res

    picking_type_id = fields.Many2one('stock.picking.type', 'Deliver To', required=True,
    domain=lambda self: [('id', 'in', self.get_restrict_picking_type()),
    ('warehouse_id', 'in', self.get_restrict_warehouse())],
    help="This will determine operation type of incoming shipment")
