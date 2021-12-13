from odoo import fields, models, api, tools, _
from odoo.tools.misc import formatLang

class SaleOrder(models.Model):
    _inherit = 'sale.order'
