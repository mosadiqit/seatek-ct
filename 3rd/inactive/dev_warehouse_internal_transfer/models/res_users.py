# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Devintelle Software Solutions (<http://devintellecs.com>).
#
##############################################################################

from odoo import models, fields, api, _

class res_users(models.Model):
    _inherit = 'res.users'
    
    tag_ids = fields.Many2many('product.warehouse.tags',string='Tags')
    
    



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
