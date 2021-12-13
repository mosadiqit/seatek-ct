# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.tools import remove_accents

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.depends('name')
    def _compute_unaccent_name(self):
        for product in self:
            product.name_unaccent = remove_accents(product.name)

    name_unaccent = fields.Char('Unaccent of name', compute='_compute_unaccent_name', store=True)

class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        if not args:
            args = []
        products = self.search([('name_unaccent', 'ilike', name)] + args, limit=limit).name_get() if name else []
        return list(set(products + super(ProductProduct, self)._name_search(name, args, operator, limit, name_get_uid)))
