# -*- coding: utf-8 -*-

from odoo import models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    requisition_id = fields.Many2one(
        'requisition.order',
        string='Requisition Order',
        readonly=True,
    )
