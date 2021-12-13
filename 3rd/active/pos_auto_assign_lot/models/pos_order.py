# -*- coding: utf-8 -*-

import logging
from datetime import timedelta
from functools import partial

import psycopg2
import pytz

from odoo import api, fields, models, tools, _
from odoo.tools import float_is_zero
from odoo.exceptions import UserError
from odoo.http import request
from odoo.addons import decimal_precision as dp
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    
    _inherit = "pos.order"
    
    def _is_ready_to_be_validated(self,picking):
        is_ready = True
        for stock_move in picking.move_lines.filtered(lambda x : x.product_id.tracking != 'none'):
            required_quantity = stock_move.product_uom_qty
            reserved_quantity = 0
            for stock_move_line in stock_move.move_line_ids:
                reserved_quantity += stock_move_line.product_uom_qty
                stock_move_line.write({'qty_done':stock_move_line.product_uom_qty})
            if float_compare(required_quantity, reserved_quantity,
                                 precision_rounding=stock_move.product_uom.rounding):
                is_ready = False
        return is_ready
    
    def _force_picking_done(self, picking):
        """Force picking in order to be set as done."""
        self.ensure_one()
        picking.action_assign()
        wrong_lots = self.set_pack_operation_lot(picking)
        is_ready = self._is_ready_to_be_validated(picking)
        if is_ready:
            picking.action_done()
