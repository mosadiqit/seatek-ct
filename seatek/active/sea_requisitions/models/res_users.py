# -*- coding: utf-8 -*-

from odoo import models, fields

class ResUser(models.Model):
    _inherit = 'res.users'

    dest_location_id = fields.Many2one(
        'stock.location',
        string='Destination Location',
    )
