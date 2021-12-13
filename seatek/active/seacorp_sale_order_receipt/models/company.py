from odoo import fields, models, api, tools, _
from odoo.tools.misc import formatLang

class Company(models.Model):
    _inherit = 'res.company'

    so_receipt_header = fields.Html('Receipt Header')
