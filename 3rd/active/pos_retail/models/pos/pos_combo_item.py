# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class pos_combo_item(models.Model):
    _name = "pos.combo.item"
    _rec_name = "name"
    _description = "Management Product Pack/Combo"

    name = fields.Char('Name', required=1)
    required = fields.Boolean('Is Required', default=0)
    product_combo_id = fields.Many2one(
        'product.template',
        'Product Template',
        required=True,
        domain=[('available_in_pos', '=', True)]
    )
    product_ids = fields.Many2many(
        'product.product',
        'combo_item_product_rel',
        'combo_item_id',
        'product_id',
        string='Products', required=True,
        domain=[('available_in_pos', '=', True), ('type', '=', 'product')])
    quantity = fields.Float(
        'No. of Items',
        help='Total quantities can add to Line',
        required=1, default=1)

    @api.model
    def create(self, vals):
        if vals.get('quantity', 0) < 0:
            raise UserError('Quantity can not smaller 0')
        return super(pos_combo_item, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get('quantity', 0) < 0:
            raise UserError('Quantity can not smaller 0')
        return super(pos_combo_item, self).write(vals)
