from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def get_address_format(self, partner):
        address = ""
        if partner.street:
           address += ", " + partner.street
        if partner.street2:
            address += ", " + partner.street2
        if partner.city:
            address += ", " + partner.city
        if len(address) > 2:
            address = address[2:]
        return address