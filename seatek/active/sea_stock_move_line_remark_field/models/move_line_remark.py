# -*- coding: utf-8 -*-
from odoo import models, fields, api


class StockMoveLineRemark(models.Model):
    _inherit = "stock.move.line"

    # remarks = fields.Char('Remark')
    remarks = fields.Text(string='Remarks', store=True, default="")