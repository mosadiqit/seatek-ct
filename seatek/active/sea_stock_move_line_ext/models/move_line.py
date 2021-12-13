# -*- coding: utf-8 -*-
from odoo import models, fields, api


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    origin = fields.Char(related='move_id.origin', string='Source', store=False)