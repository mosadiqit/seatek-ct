from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    sale_quotation_order = fields.Many2one('ir.ui.view')