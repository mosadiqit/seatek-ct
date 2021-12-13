from odoo import models
from odoo.addons.global_seatek import Seatek

from odoo.fields import Datetime


class StockPicking(models.Model, Seatek):
    _inherit = "stock.picking"

    def getReportName(self):
        # self.env['ir.translation'].get_field_string(self.picking_type_code.ref_class)[self.picking_type_code.ref_field]
        if self.picking_type_code == 'incoming':
            title = "RECEIPT NOTE"
        elif self.picking_type_code == 'outgoing':
            title = "DELIVERY NOTE"
        else:
            title = "INTERNAL TRANSFER"
        translations = self.env['ir.translation'].search([
            ('module', '=', 'sc_stock_report_pdf'),
            ('src', '=', title),
            ('lang', '=', self.env.user.lang),
            #('res_id', '=', view.id),
        ])
        return translations.value

    def get_effective_date(self):
        if self.date_done:
            return Datetime.context_timestamp(self, self.date_done).strftime( "Ngày %d tháng %m") + " năm " + Datetime.context_timestamp(self, self.date_done).strftime("%Y")

        return ""

    def get_partner_from(self):
        if self.location_id.usage == 'customer':
            if self.partner_id.parent_id.name:
                return str(self.partner_id.parent_id.name) + ', ' + str(self.partner_id.name)
            return str(self.partner_id.name)

        elif self.location_id.usage == 'supplier':
            if self.partner_id.parent_id.name:
                return str(self.partner_id.parent_id.name) + ', ' + str(self.partner_id.name)
            return str(self.partner_id.name)

        return str(self.location_id.location_id.name) + '/' + str(self.location_id.name)

    def get_partner_to(self):
        if self.location_dest_id.usage == 'customer':
            if self.partner_id.parent_id.name:
                return str(self.partner_id.parent_id.name) + ', ' + str(self.partner_id.name)
            return str(self.partner_id.name)

        elif self.location_dest_id.usage == 'supplier':
            if self.partner_id.parent_id.name:
                return str(self.partner_id.parent_id.name) + ', ' + str(self.partner_id.name)
            return str(self.partner_id.name)

        return str(self.location_dest_id.location_id.name) + '/' + str(self.location_dest_id.name)

    def get_partner_to_add(self):
        if self.partner_id:
            if self.partner_id.parent_id.name:
                return str(self.partner_id.parent_id.name) + ', ' + str(self.partner_id.name)
            return str(self.partner_id.name)

        return str(self.location_id.location_id.name) + '/' + str(self.location_id.name)

    def get_partner_to_out(self):
        if self.partner_id:
            if self.partner_id.parent_id.name:
                return str(self.partner_id.parent_id.name) + ', ' + str(self.partner_id.name)
            return str(self.partner_id.name)

        return str(self.location_dest_id.location_id.name) + '/' + str(self.location_dest_id.name)