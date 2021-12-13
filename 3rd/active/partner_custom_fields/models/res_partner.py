#coding: utf-8

from odoo import fields, models


class res_partner(models.Model):
    """
    Overwrite to add type
    """
    _inherit = "res.partner"

    custom_type_id = fields.Many2one(
        "partner.custom.type",
        string="Partner Type",
    )
