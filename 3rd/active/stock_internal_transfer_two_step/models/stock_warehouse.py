# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class Warehouse(models.Model):
    _inherit = 'stock.warehouse'

    internal_transfer_location_id = fields.Many2one('stock.location', 'Internal transit location', domain=[('usage', '=', 'transit')])
    user_permis_ids = fields.Many2many('res.users', 'tgl_partner_permis_user_rel', string='Permission to Send and Receive Products')
    enable_auto_split = fields.Boolean(string='Auto split quantity when internal transfer')

    @api.model
    def create(self, vals):
        res = super(Warehouse, self).create(vals)
        transit_location = self.env['stock.location'].create({
            'name': 'Transit',
            'usage': 'transit',
            'location_id': res.view_location_id.id
        })
        res.internal_transfer_location_id = transit_location.id
        return res

    def tgl_create_transit_location(self):
        LocationObj = self.env['stock.location']
        for warehouse in self:
            transit_location = LocationObj.search([('usage', '=', 'transit'), ('location_id', '=', warehouse.view_location_id.id)], limit=1)
            if not transit_location:
                transit_location = LocationObj.create({
                    'name': 'Transit',
                    'usage': 'transit',
                    'location_id': warehouse.view_location_id.id
                })
            warehouse.internal_transfer_location_id = transit_location.id

        # Update view
        PickingObj = self.env['stock.picking']
        pickings = PickingObj.sudo().search([('picking_type_code', '=', 'internal'), ('tgl_vitual_location_id', '=', False)])
        for picking in pickings:
            picking.write({
                'tgl_vitual_location_id': picking.location_id.id,
                'tgl_vitual_location_dest_id': picking.location_dest_id.id,
            })
