from odoo import models, api


# class ReportSaleSummaryReportView(models.AbstractModel):
#     """
#         Abstract Model specially for report template.
#         _name = Use prefix `report.` along with `module_name.report_name`
#     """
#     _name = 'report.sc_stock_report_pdf.sc_stock_sale_delivery_templates'
#
#     def _get_report_values(self, docids, data=None):
#         pickings = self.env['stock.picking'].browse(docids)
#         # for p in pickings:
#         #     sale = p.sale_id
#         #     if sale:
#         #         total_discount = 0
#         #         amount_total = 0
#         #         for l in sale.order_line:
#         #             if l.display_type is False:
#         #                 if l.price_total_without_discount == 0:
#         #                     l.price_total_without_discount = l.qty_delivered * l.price_unit
#         #                     l.price_discount = (l.price_total_without_discount * l.discount)/100
#         #                     total_discount += l.price_discount
#         #                     l.sea_price_total_qty_delivered = l.price_total_without_discount - l.price_discount
#         #                 amount_total += l.sea_price_total_qty_delivered
#         #         sale.total_discount = total_discount
#         #         sale.total_amount_qty_delivery = amount_total
#
#         return {
#             'doc_ids': docids,
#             'doc_model': 'stock.picking',
#             'docs': pickings,
#         }
