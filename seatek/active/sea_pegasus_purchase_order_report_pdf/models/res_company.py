from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    purchase_order_report = fields.Many2one('ir.ui.view')
