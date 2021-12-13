# -*- encoding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _


class StockPicking(models.Model):
    _inherit = "stock.picking"

    get_product_ean = fields.Char(string='Add Product', size=13, help="Read a product barcode to add it as new Line.")
    message = fields.Char(string='Message', help="Warning message.")

    @api.onchange('get_product_ean')
    def onchange_product_ean(self):
        self.message = ''
        if not self.get_product_ean:
            return

        ProductObj = self.env['product.product']
        LotObj = self.env['stock.production.lot']
        Line = self.env['stock.move']
        #Check first Lot
        lot = LotObj.search([('name','=',self.get_product_ean)], limit=1)
        if lot:
            product = lot.product_id
        else:
            product = ProductObj.search([('barcode','=',self.get_product_ean)], limit=1)
            if not product:
                product = ProductObj.search([('default_code','=',self.get_product_ean)], limit=1)
            if not product:
                warning = {'title': _('Warning!'),
                    'message': _("There is no product with Lot, Barcode or Reference: %s") % (self.get_product_ean),
                }
                self.get_product_ean = False
                return {'warning': warning}

        flag = 1
        for o_line in self.move_ids_without_package:
            if o_line.product_id == product:
                o_line.product_uom_qty = o_line.product_uom_qty + 1
                flag = 0
        if flag:
            self.move_ids_without_package += Line.new({
                'product_id': product.id,
                'product_uom_qty' : 1,
                'name': product.name,
                'product_uom': product.uom_id.id,
                'state': 'draft',
                'picking_type_id': self.picking_type_id and self.picking_type_id.id or False,
                'location_id': self.location_id and self.location_id.id or False,
                'location_dest_id': self.location_dest_id and self.location_dest_id.id or False,
                'date_expected': fields.Datetime.now(),
            })
        self.get_product_ean = False

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: 
