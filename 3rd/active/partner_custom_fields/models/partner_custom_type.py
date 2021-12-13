#coding: utf-8

from odoo import fields, models


class partner_custom_type(models.Model):
    """
    The model to classify partner by types (for custom fields attributes)
    """
    _inherit = "custom.field.type"
    _name = "partner.custom.type"
    _description = "Partner Type"
    _custom_field_model = ["custom.partner.field"]

    custom_fields_ids = fields.Many2many(
        "custom.partner.field",
        "partner_custom_type_custom_partner_field_reltable",
        "custom_partner_field_rel_id",
        "partner_custom_type_rel_id",
        string="Custom Fields",
    )
