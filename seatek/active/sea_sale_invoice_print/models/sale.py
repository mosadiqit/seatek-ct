from odoo import models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def get_effective_date(self):
        if self.effective_date:
            return self.effective_date.strftime("Ngày %d tháng %m năm %Y")
        return ""


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def _prepare_invoice_line(self, qty):
        vals = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        vals['remarks'] = self.remarks
        return vals
