from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    sale_delivery_note = fields.Many2one('ir.ui.view')