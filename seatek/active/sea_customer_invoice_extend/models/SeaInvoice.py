from odoo import models, fields, api

class SeaInvoice(models.Model):
    _inherit = 'account.invoice'

    sea_vat_no = fields.Char(string='Vat Number', store=True, default="")
    sea_settlement_code = fields.Char(string='Settlement Code', store=True, default="")

