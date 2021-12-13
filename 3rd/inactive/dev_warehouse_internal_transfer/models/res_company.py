# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Devintelle Software Solutions (<http://devintellecs.com>).
#
##############################################################################

from odoo import models, fields, api, _

class res_company(models.Model):
    _inherit = 'res.company'
    
    transit_location_id = fields.Many2one('stock.location',string='Transit Location', domain=[('usage','=','transit')])
    
    



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
