# -*- coding: utf-8 -*-

from odoo import fields, models


class custom_partner_field(models.Model):
    _name = 'custom.partner.field'
    _inherit = ["custom.extra.field"]
    _description = 'Custom Partner Field'
    _field_code = "prtn"
    _linked_model = "res.partner"
    _type_field = "custom_type_id"
    _type_field_model = "partner.custom.type"
    _backend_views = ["partner_custom_fields.res_partner_view_form"]

    types_ids = fields.Many2many(
        "partner.custom.type",
        "partner_custom_type_custom_partner_field_reltable",
        "partner_custom_type_rel_id",
        "custom_partner_field_rel_id",
        string="Types",
        help="Leave it empty, if this field should appear for all partners disregarding type"
    )
    placement = fields.Selection(
        selection_add=[
            ("left_panel_group", "Left Column"),
            ("right_panel_group", "Rigth Column"),
            ("after_description_group", "After Internal Notes"),
            ("details_group_custom_fields", "Sales and Purchase Tab"),
        ]
    )
    sel_options_ids = fields.One2many(context={'default_model': "custom.partner.field"},)
