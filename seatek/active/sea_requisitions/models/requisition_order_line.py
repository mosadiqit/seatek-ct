# -*- coding: utf-8 -*-
from odoo import models, fields, api
import odoo.addons.decimal_precision as dp

class MaterialPurchaseRequisitionLine(models.Model):
    _name = "requisition.order.line"
    _description = 'Requisition Order Line'
    
    requisition_id = fields.Many2one('requisition.order', string='Requisitions',)
    product_id = fields.Many2one('product.product', string='Product', required=True,)
#    layout_category_id = fields.Many2one('sale.layout_category', string='Section',)
    description = fields.Char(string='Description', required=True,)
    qty = fields.Float(string='Quantity', default=1, required=True,)
    uom = fields.Many2one('uom.uom', string='Unit of Measure', required=True,)
    partner_id = fields.Many2many('res.partner', string='Vendors',)
    requisition_type = fields.Selection(string='Requisition Action', default='internal', required=True, selection=[
                    ('internal','Internal Picking'),
                    ('purchase','Purchase Order'),
                    ],)
    @api.onchange('product_id')
    def onchange_product_id(self):
        for rec in self:
            rec.description = rec.product_id.name
            rec.uom = rec.product_id.uom_id.id
