from odoo import models, fields


class SeaPuchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    sea_hscode = fields.Text(string='HS Code', store=True, default="")


class SeaPuchaseOrder(models.Model):
    _inherit = 'purchase.order'

    sea_vessel_name = fields.Many2one('res.partner', string='Vessel Name', readonly=True,
                                      states={'draft': [('readonly', False)], 'sent': [('readonly', False)],
                                              'sale': [('readonly', False)]}, help="Vessel Name",
                                      domain="[('type','=','ship')]")
