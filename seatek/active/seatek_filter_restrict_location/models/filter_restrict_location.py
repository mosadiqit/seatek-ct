# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_round


class FilterRetrictLocation(models.Model):
    _inherit = "stock.picking"
    _description = "Filter Retrict Location"

    @api.multi
    def get_restrict_location(self):
        if 'stock_location_ids' in self.env.user:
            res = []
            for item in self.env.user.stock_location_ids:
                res.append(item.id)
            return res

    location_id = fields.Many2one(
        'stock.location', "Source Location",
        domain=lambda self: [('id', 'in', self.get_restrict_location())],
        default=lambda self: self.env['stock.picking.type'].browse(self._context.get('default_picking_type_id')).default_location_dest_id,
        readonly=True, required=True,
        states={'draft': [('readonly', False)]})
    location_dest_id = fields.Many2one(
        'stock.location', "Destination Location",
        domain=lambda self: [('id', 'in', self.get_restrict_location())],
        default=lambda self: self.env['stock.picking.type'].browse(self._context.get('default_picking_type_id')).default_location_dest_id,
        readonly=True, required=True,
        states={'draft': [('readonly', False)]})