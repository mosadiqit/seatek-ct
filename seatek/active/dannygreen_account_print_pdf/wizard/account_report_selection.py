from odoo import models, fields, api
from odoo.exceptions import ValidationError


class StockReportSelection(models.TransientModel):
    _name = 'dannygreen.account.report.selection'
    _description = 'Select option report'

    selection_report = fields.Selection(lambda self: self._get_selection_report(), string="Selection")

    def _get_selection_report(self):
        return [
            ('dannygreen_account_invoicing_sale_slip_report', 'Phiếu bán hàng ký gửi')
            # ('dannygreen_account_invoicing_sale_xuat_kho_giao_nhan', 'Phiếu xuất kho kiêm giao nhận hàng hóa'),
        ]

    @api.multi
    def print(self):
        self.ensure_one()
        if self.selection_report:
            [data] = self.read()
            data['invoice'] = self.env.context.get('active_ids', [])
            invoices = self.env['account.invoice'].browse(data['invoice'])
            # for i in invoices:
            #     total_discount = 0
            #     for l in i.invoice_line_ids:
            #         total = l.price_total * 100 / (100 - l.discount)
            #         l.price_discount = total - l.price_total
            #         l.price_total_without_discount = total
            #         total_discount += l.price_discount
            #     i.total_discount = total_discount
            # datas = {
            #     'ids': data['picking'],
            #     'model': 'stock.picking',
            #     'form': data
            # }
            return self.env.ref('dannygreen_account_print_pdf.%s' % self.selection_report).report_action(invoices)
        else:
            raise ValidationError("Please select a report type")
