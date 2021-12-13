# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import Warning
from odoo.addons.purchase.models.purchase import PurchaseOrder as Purchase


class FilterPurchaseStock(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def _default_picking_type(self):
        type_obj = self.env['stock.picking.type']
        company_id = self.env.context.get('company_id') or self.env.user.company_id.id
        types = type_obj.search([('code', '=', 'incoming'), ('warehouse_id.company_id', '=', company_id)])
        if not types:
            types = type_obj.search([('code', '=', 'incoming'), ('warehouse_id', '=', False)])
        return types[:1]

    @api.multi
    def get_domain_operation_type(self):
        if 'warehouse_ids' in self.env.user:
            res = []
            for item in self.env.user.warehouse_ids:
                res.append(item.id)
            return res

    picking_type_id = fields.Many2one('stock.picking.type', 'Deliver To', 
    states=Purchase.READONLY_STATES, required=True, default=_default_picking_type,
    domain=lambda self: [('warehouse_id', 'in', self.get_domain_operation_type())],
    help="This will determine operation type of incoming shipment")
