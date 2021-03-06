# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.addons import decimal_precision as dp
from odoo.exceptions import ValidationError
from odoo.tools import float_compare


class StockMoveLocationWizardLine(models.TransientModel):
    _name = "wiz.stock.move.location.line"
    _description = 'Wizard move location line'

    wizart_id = fields.Many2one(string="Stock line ids", comodel_name="wiz.stock.move.location")
    origin_location_id = fields.Many2one(string='Origin Location', comodel_name='stock.location')
    product_id = fields.Many2one(string="Product", comodel_name="product.product", required=True,)
    destination_location_id = fields.Many2one(string='Destination Location', comodel_name='stock.location',)
    product_uom_id = fields.Many2one(string='Product Unit of Measure', comodel_name='uom.uom',)
    lot_id = fields.Many2one(string='Lot/Serial Number', comodel_name='stock.production.lot', domain="[('product_id','=',product_id)]")
    move_quantity = fields.Float(string="Quantity to move", digits=dp.get_precision('Product Unit of Measure'),)
    max_quantity = fields.Float(string="Maximum available quantity", digits=dp.get_precision('Product Unit of Measure'),)
    custom = fields.Boolean(string="Custom line", default=True)
    tracking = fields.Char(compute='_compute_tracking')

    remain_quantity = fields.Float(string="Remain quantity", digits=dp.get_precision('Product Unit of Measure'),)

    @api.depends('product_id', 'product_id.tracking')
    def _compute_tracking(self):
        for record in self:
            record.tracking = record.product_id and record.product_id.tracking or False

    @api.onchange('product_id', 'lot_id')
    def _onchange_product_id(self):
        self.product_uom_id = self.product_id.uom_id
        search_args = [
            ('location_id', '=', self.origin_location_id.id),
            ('product_id', '=', self.product_id.id),
        ]
        if self.lot_id:
            search_args.append(('lot_id', '=', self.lot_id.id))
        else:
            search_args.append(('lot_id', '=', False))
        res = self.env['stock.quant'].read_group(search_args, ['quantity'], [])
        max_quantity = res[0]['quantity']
        self.max_quantity = max_quantity

        res = self.env['internal.stock.move'].read_group([
            ('product_id', '=', self.product_id.id), ('picking_id', '=', self.wizart_id.picking_id.id)],
            ['move_send_done', 'move_receipt_done', 'max_quantity'], [])
        if res and res[0]:
            if self._context.get('is_receipt'):
                self.remain_quantity = (res[0].get('max_quantity') or 0) - (res[0].get('move_receipt_done') or 0)
            else:
                self.remain_quantity = (res[0].get('max_quantity') or 0) - (res[0].get('move_send_done') or 0)

    @staticmethod
    def _compare(qty1, qty2, precision_rounding):
        return float_compare(
            qty1, qty2,
            precision_rounding=precision_rounding)

    @api.constrains("max_quantity", "move_quantity")
    def _constraint_max_move_quantity(self):
        for record in self:
            rounding = record.product_uom_id.rounding
            # move_qty_gt_max_qty = self._compare(record.move_quantity, record.max_quantity, rounding) == 1
            move_qty_lt_0 = self._compare(record.move_quantity, 0.0, rounding) == -1
            # if (move_qty_gt_max_qty or move_qty_lt_0):
            if move_qty_lt_0:
                raise ValidationError(_(
                    "Move quantity can not exceed max quantity!"
                ))

    def get_max_quantity(self):
        self.product_uom_id = self.product_id.uom_id
        search_args = [
            ('location_id', '=', self.origin_location_id.id),
            ('product_id', '=', self.product_id.id),
        ]
        if self.lot_id:
            search_args.append(('lot_id', '=', self.lot_id.id))
        else:
            search_args.append(('lot_id', '=', False))
        res = self.env['stock.quant'].read_group(search_args, ['quantity'], [])
        max_quantity = res[0]['quantity']
        return max_quantity

    def create_move_lines(self, picking, move):
        for line in self:
            values = line._get_move_line_values(picking, move)
            if not self.env.context.get("planned") and \
                    values.get("qty_done") <= 0:
                continue
            self.env["stock.move.line"].create(
                values
            )
        return True

    def _get_move_line_values(self, picking, move):
        self.ensure_one()
        # location_dest_id = self.destination_location_id.get_putaway_strategy(self.product_id).id or self.destination_location_id.id
        location_dest_id = self.destination_location_id.id

        stock_piking = self.env['stock.picking'].browse(
            self.env.context.get('active_ids'))
        picking_line = stock_piking.internal_move_ids.search([
                ('product_id', '=', self.product_id.id),
                ('picking_id', '=', picking.id),
                # ("lot_id" , '=', self.lot_id.id),
                ], limit=1)

        if (self._context.get('is_receipt')):
            picking_line.write({
                    'move_receipt_done': picking_line.move_receipt_done + self._get_available_quantity(),
                    # 'lot_id':  self.lot_id.id,
                })
        else:
            picking_line.write({
                    'move_send_done': picking_line.move_send_done + self._get_available_quantity(),
                    # 'lot_id':  self.lot_id.id,
                })

        return {
            "product_id": self.product_id.id,
            "lot_id": self.lot_id.id,
            "location_id": self.origin_location_id.id,
            "location_dest_id": location_dest_id,
            "qty_done": self._get_available_quantity(),
            "product_uom_id": self.product_uom_id.id,
            "picking_id": picking.id,
            "move_id": move.id,
        }

    def _get_available_quantity(self):
        """We check here if the actual amount changed in the stock.

        We don't care about the reservations but we do care about not moving
        more than exists."""
        self.ensure_one()
        if not self.product_id:
            return 0
        if self.env.context.get("planned"):
            # for planned transfer we don't care about the amounts at all
            return 0.0
        if not self.lot_id:
            return self.move_quantity

        search_args = [
            ('location_id', '=', self.origin_location_id.id),
            ('product_id', '=', self.product_id.id),
        ]
        if self.lot_id:
            search_args.append(('lot_id', '=', self.lot_id.id))
        else:
            search_args.append(('lot_id', '=', False))
        res = self.env['stock.quant'].read_group(search_args, ['quantity'], [])
        available_qty = res[0]['quantity']
        if not available_qty:
            # if it is immediate transfer and product doesn't exist in that
            # location -> make the transfer of 0.
            return 0
        rounding = self.product_uom_id.rounding
        available_qty_lt_move_qty = self._compare(available_qty, self.move_quantity, rounding) == -1
        if available_qty_lt_move_qty:
            return available_qty
        return self.move_quantity
