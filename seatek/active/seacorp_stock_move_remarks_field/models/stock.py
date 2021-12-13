# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleMove(models.Model):
    _inherit = 'stock.move'

    remarks = fields.Text(related="sale_line_id.remarks", string='Remarks', store=True, default="")
