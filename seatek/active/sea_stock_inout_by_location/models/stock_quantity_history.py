# -*- coding: utf-8 -*-
import pytz

from odoo import api, fields, models, _, exceptions
from odoo.fields import Datetime


class ScStockQuantityHistory(models.TransientModel):
    _inherit = "stock.quantity.history"

    # compute_at_date = fields.Selection(selection_add=[(2, 'From date to date')])
    from_date = fields.Datetime('Inventory from Date', help="Choose a date to get the inventory from that date",
                                default=fields.Datetime.now)

    location_ids = fields.Many2many('stock.location', string='Địa điểm kho', domain=[('usage', 'in', ('internal', 'transit'))])

    def open_table_from_to_date(self):
        self.ensure_one()
        Quant = self.env['stock.quant']
        ProductReport = self.env['product.report']
        # TRUNCATE TABLE orders CASCADE
        self.env.cr.execute("TRUNCATE TABLE product_report RESTART IDENTITY")
        # ProductReport.search([]).unlink()
        domain = []
        if self.location_ids:
            domain += [('location_id', 'in', list(loc.id for loc in self.location_ids))]
        list_quant = Quant.search(domain)
        for i in list_quant:
            print(i)
            ProductReport.create({
                'product_id': i.product_id.id,
                'location_id': i.location_id.id,
                'quantity': i.quantity,
                'product_uom': i.product_id.uom_id.id,
                'company_id': i.company_id.id,
                'lot_id': i.lot_id.id,
                'package_id': i.package_id.id,
                'owner_id': i.owner_id.id,
                'reserved_quantity': i.reserved_quantity,
            })

        if self.from_date < self.date:
            domain_move_in = domain_move_out = []
            if self.date:
                dt_to = Datetime.context_timestamp(self, self.date).replace(minute=59, hour=23, second=59)
                dt_to = dt_to.astimezone(pytz.utc)
                self.date = dt_to.replace(tzinfo=None)
                domain_move_in += [('date', '=', self.date)]
                domain_move_out += [('date', '=', self.date)]
            if self.from_date:
                dt_from = Datetime.context_timestamp(self, self.from_date).replace(hour=0, minute=0, second=0)
                dt_from = dt_from.astimezone(pytz.utc)
                self.date_from = dt_from.replace(tzinfo=None)
                domain_move_in += [('date', '=', self.from_date)]
                domain_move_out += [('date', '=', self.from_date)]


            tree_view_id = self.env.ref('sea_stock_inout_by_location.sea_view_stock_product_report_tree').id
            # form_view_id = self.env.ref('stock.product_form_view_procurement_button').id
            # We pass `to_date` in the context so that `qty_available` will be computed across
            # moves until date.
            action = {
                'type': 'ir.actions.act_window',
                'views': [(tree_view_id, 'tree')],
                'view_mode': 'tree,form',
                'name': _('Products Report'),
                'res_model': 'product.report',
                'domain': domain,
                'context': dict(self.env.context, to_date=self.date, from_date=self.from_date),
            }
            return action
        else:
            raise exceptions.ValidationError("From date must less than to date")
            return {}

    @api.onchange("from_date", "date")
    def validateDate(self):
        if self.from_date:
            if self.from_date > self.date:
                raise exceptions.ValidationError("From date must less than to date")
