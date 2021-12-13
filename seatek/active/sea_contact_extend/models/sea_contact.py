# -*- coding: utf-8 -*-
from odoo import api, fields, models

class SeaContact(models.Model):
    _inherit = 'res.partner'
    # Ma Kinh Doanh from PhiMa
    sea_business_code = fields.Char(string='Business Code', copy=False)
    type = fields.Selection(
        [('contact', 'Contact'),
         ('invoice', 'Invoice address'),
         ('delivery', 'Shipping address'),
         ('other', 'Other address'),
         ("private", "Private Address"),
         ("ship", "Ship"),
         ], string='Address Type',
        default='contact',
        help="Used by Sales and Purchase Apps to select the relevant address depending on the context.")
