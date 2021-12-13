# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ProductExtend(models.Model):
    _inherit = 'product.product'

    sea_product_variant_name = fields.Char(string='Product Variant Name', copy=False)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    #@api.onchange('product_id')
    def get_sale_order_line_multiline_description_sale(self, product):
            if product.sea_product_variant_name:
               return product.sea_product_variant_name
            else:
                return super(SaleOrderLine, self).get_sale_order_line_multiline_description_sale(product)

