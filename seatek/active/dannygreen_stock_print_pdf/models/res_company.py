from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    dannygreen_stock_form_report = fields.Boolean("DannyGreen Form report", default=False)
