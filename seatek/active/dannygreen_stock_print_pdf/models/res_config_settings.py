# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # company_id = fields.Many2one('res.company', string='Company', required=False,
    #                              default=lambda self: self.env.user.company_id)

    dannygreen_stock_form_report = fields.Boolean(related="company_id.dannygreen_stock_form_report", readonly=False)
