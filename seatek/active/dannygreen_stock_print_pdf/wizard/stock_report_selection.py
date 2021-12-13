from odoo import models, fields, api
from odoo.exceptions import ValidationError


class StockReportSelection(models.TransientModel):
    _name = 'stock.report.selection'
    _description = 'Select option report'

    selection_report = fields.Selection(lambda self: self._get_selection_report(), string="Selection")

    def _get_selection_report(self):
        return [
            ('dannygreen_stock_action_out_inventory_report', 'Phiếu xuất kho ký gửi'),
            ('dannygreen_stock_action_in_inventory_report', 'Phiếu nhập kho ký gửi')
        ]

    @api.multi
    def print(self):
        self.ensure_one()
        if self.selection_report:
            [data] = self.read()
            data['picking'] = self.env.context.get('active_ids', [])
            pickings = self.env['stock.picking'].browse(data['picking'])
            for picking in pickings:
                sale = picking.sale_id
                if sale:
                    sale_lines = dict((l.product_id, l) for l in sale.order_line)
                    total = 0
                    for move in picking.move_ids_without_package:
                        if move.product_id in sale_lines:
                            line = sale_lines[move.product_id]
                            if line:
                                move.price_total = line.price_unit * (1 - (line.discount or 0.0) / 100.0) * move.quantity_done
                                total += move.price_total
                    picking.amount_total = total

            # datas = {
            #     'ids': data['picking'],
            #     'model': 'stock.picking',
            #     'form': data
            # }
            return self.env.ref('dannygreen_stock_print_pdf.%s' % self.selection_report).report_action(pickings)
        else:
            raise ValidationError("Please select a report type")
