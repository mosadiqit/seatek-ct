# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, exceptions


class ScStockQuantityHistory(models.TransientModel):
    _inherit = "stock.quantity.history"

    # compute_at_date = fields.Selection(selection_add=[(2, 'From date to date')])
    from_date = fields.Datetime('Inventory from Date', help="Choose a date to get the inventory from that date",
                                default=fields.Datetime.now)

    def open_table_from_to_date(self):
        self.ensure_one()

        if self.from_date < self.date:
            tree_view_id = self.env.ref('sc_stock_report_view.sc_view_stock_product_tree').id
            form_view_id = self.env.ref('stock.product_form_view_procurement_button').id
            # We pass `to_date` in the context so that `qty_available` will be computed across
            # moves until date.
            action = {
                'type': 'ir.actions.act_window',
                'views': [(tree_view_id, 'tree'), (form_view_id, 'form')],
                'view_mode': 'tree,form',
                'name': _('Products'),
                'res_model': 'product.product',
                'domain': "[('type', '=', 'product')]",
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
