# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Devintelle Software Solutions (<http://devintellecs.com>).
#
##############################################################################

from odoo import models, fields, api, exceptions, _

class res_config_settings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    transit_location_id = fields.Many2one(related='company_id.transit_location_id',string='Transit Location', 
                                          domain=[('usage','=','transit')],  readonly=False)
    
    



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
