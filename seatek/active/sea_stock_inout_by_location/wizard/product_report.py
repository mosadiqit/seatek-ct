from odoo import models, fields, exceptions, api, _
from odoo.addons import decimal_precision as dp
from odoo.addons.stock.models.stock_quant import StockQuant


class ProductReportWizard(models.TransientModel):
    _name = "product.report"
    _description = "Product Report"

    product_id = fields.Many2one(
        'product.product', 'Product',
        ondelete='restrict', readonly=True, required=True, index=True)
    product_uom = fields.Many2one('uom.uom', 'Unit of Measure')

    company_id = fields.Many2one(related='location_id.company_id',
                                 string='Company', store=True, readonly=True)
    location_id = fields.Many2one(
        'stock.location', 'Location',
        auto_join=True, ondelete='restrict', readonly=True, index=True)
    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial Number',
        ondelete='restrict', readonly=True)
    package_id = fields.Many2one(
        'stock.quant.package', 'Package',
        help='The package containing this quant', readonly=True, ondelete='restrict')
    owner_id = fields.Many2one(
        'res.partner', 'Owner',
        help='This is the owner of the quant', readonly=True)
    quantity = fields.Float(
        'Quantity',
        help='Quantity of products in this quant, in the default unit of measure of the product',
        readonly=True, required=True)
    reserved_quantity = fields.Float(
        'Reserved Quantity',
        default=0.0,
        help='Quantity of reserved products in this quant, in the default unit of measure of the product',
        readonly=True)

    early_period_available = fields.Float(
        'Available of early period', compute='compute_early_period', search='_search_early_period_available',
        digits=dp.get_precision('Product Unit of Measure'))

    end_period_available = fields.Float(
        'Available of the end period', compute='compute_end_period', search='_search_end_period_available',
        digits=dp.get_precision('Product Unit of Measure'))

    def open_table_from_to_date(self):
        self.ensure_one()
        print("open_table_from_to_date")
        Quant = self.env['stock.quant']
        for i in Quant.browse():
            print(i)
            # self.create({
            #     'product_id': i.product_id
            # })

        if self.from_date < self.date:
            tree_view_id = self.env.ref('sea_stock_inout_by_location.sea_view_stock_product_report_tree').id
            # form_view_id = self.env.ref('stock.product_form_view_procurement_button').id
            # We pass `to_date` in the context so that `qty_available` will be computed across
            # moves until date.
            self.env['product.report'].create()
            action = {
                'type': 'ir.actions.act_window',
                'views': [(tree_view_id, 'tree')],
                'view_mode': 'tree',
                'name': _('Product'),
                'res_model': 'product.report',
                # 'domain': "[('type', '=', 'product')]",
                'context': dict(self.env.context, to_date=self.to_date, from_date=self.from_date,
                                location_ids=self.location_ids),
            }
            return action
        else:
            raise exceptions.ValidationError("From date must less than to date")
            return {}

    @api.onchange("from_date", "to_date")
    def validateDate(self):
        if self.from_date:
            if self.from_date > self.to_date:
                raise exceptions.ValidationError("From date must less than to date")
