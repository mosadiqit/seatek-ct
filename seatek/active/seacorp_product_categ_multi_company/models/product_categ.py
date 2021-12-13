# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'

    company_id = fields.Many2one('res.company', string='Công ty')
