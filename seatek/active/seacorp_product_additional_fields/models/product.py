# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    accounting_code = fields.Char(string='Accounting Code', copy=False)
    reference_code = fields.Char(string='Reference Code', copy=False)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    accounting_code = fields.Char(string='Accounting Code', copy=False)
    reference_code = fields.Char(string='Reference Code', copy=False)
