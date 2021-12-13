# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons.mrp.models.mrp_production import MrpProduction
from odoo.addons.mrp.models.stock_move import StockMoveLine


class seatek_mrp_production(models.Model):
    _inherit = ['mrp.production']

    is_add_move_line = fields.Boolean(compute='_is_add')

    def _is_add(self):
        self.is_add_move_line = self.workorder_count == self.workorder_done_count

    @api.multi
    def write(self, vals):
        print(vals)
        super().write(vals)
        if 'finished_move_line_ids' in vals:
            for ml in vals['finished_move_line_ids']:
                ml1 = ml[2]
                if ml1:
                    product_id = False
                    ml_id = False
                    qty_done = 0
                    if 'product_id' in ml1:
                        product_id = ml1['product_id']
                    if not product_id:
                        ml_id = ml[1]
                    if 'qty_done' in ml1:
                        qty_done = ml1['qty_done']
                    if qty_done != 0:
                        self._add_or_update_finished_moves(ml_id, product_id, qty_done)

        # return res

    def _add_or_update_finished_moves(self, ml_id, product_id, qty_done):
        if ml_id:
            for m in self.move_finished_ids:
                for ml in m.move_line_ids:
                    if ml.id == ml_id:
                        vals = {
                            'product_uom_qty': qty_done,
                            'qty_done': qty_done
                        }
                        m.write(vals)
                        ml.write(vals)
                        return
        else:
            product = self.env['product.product'].search([('id', '=', product_id)], limit=1)
            move = self.env['stock.move'].create({
                'name': self.name,
                'date': self.date_planned_start,
                'date_expected': self.date_planned_start,
                'picking_type_id': self.picking_type_id.id,
                'product_id': product_id,
                'product_uom': product.product_tmpl_id.uom_id.id,
                'product_uom_qty': qty_done,
                'location_id': self.product_id.property_stock_production.id,
                'location_dest_id': self.location_dest_id.id,
                'company_id': self.company_id.id,
                'production_id': self.id,
                'warehouse_id': self.location_dest_id.get_warehouse().id,
                'origin': self.name,
                'group_id': self.procurement_group_id.id,
                'propagate': self.propagate,
                'move_dest_ids': [(4, x.id) for x in self.move_dest_ids],
            })
            move._action_confirm()
            move.write({'state': 'assigned'})
            self.env['stock.move.line'].create({
                'move_id': move.id,
                'product_id': product_id,
                'product_uom_id': product.product_tmpl_id.uom_id.id,
                'product_uom_qty': qty_done,
                'qty_done': qty_done,
                'location_id': self.product_id.property_stock_production.id,
                'location_dest_id': self.location_dest_id.id,
            })
        return move

    @api.onchange('finished_move_line_ids')
    def onChange(self):
        print("change")
        for i in self.finished_move_line_ids:
            print(i.state)
