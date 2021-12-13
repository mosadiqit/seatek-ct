from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    dannygreen_account_form_report = fields.Boolean("DannyGreen Form print PDF", default=False)
