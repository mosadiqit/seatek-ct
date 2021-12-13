# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime


class stock_warehouse(models.Model):
    _inherit = 'stock.warehouse'
    
    transfer_user_ids = fields.Many2many('res.users',string='Transfer Users')
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
