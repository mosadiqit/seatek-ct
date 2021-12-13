from odoo import fields, models, api


class StockInventoryLine(models.Model):
    _inherit = 'stock.inventory.line'
    _description = 'Stock Inventory Line'

    product_id = fields.Many2one('product.product', string="Product", readonly=True)