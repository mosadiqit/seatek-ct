# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class StockQuantityReport(models.TransientModel):
    _name = 'stock.quantity.report'
    _description = 'Stock Quantity Report'

    type_product = fields.Selection([
        (0, 'Current Inventory'),
        (1, 'At a Specific Date'),
    ], string="Compute", help="Choose to analyze the current inventory or from a specific date in the past.")
    date = fields.Datetime('Inventory at Date', help="Choose a date to get the inventory at that date",
                           default=fields.Datetime.now)

