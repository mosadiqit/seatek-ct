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
from datetime import datetime
import dateutil.relativedelta
from datetime import timedelta
import calendar
from odoo.tools.misc import formatLang

class print_stock_by_location(models.AbstractModel): 
    _name = 'report.dev_stock_by_location.dev_print_stock_by_location'

    @api.multi
    def set_amount(self, amount):
        amount  = formatLang(self.env, amount)
        return amount
        
        
    @api.model
    def _get_report_values(self, docids, data=None):
        if data.get('form'):
            docs = self.env['product.template'].browse(data['form'])
        else:
            docs = self.env['product.template'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'product.template',
            'docs': docs,
            'set_amount':self.set_amount,
        }
        
class print_product_stock_by_location(models.AbstractModel): 
    _name = 'report.dev_stock_by_location.dev_pro_print_sto_by_loc'

    @api.multi
    def set_amount(self, amount):
        amount  = formatLang(self.env, amount)
        return amount
        
        
    @api.model
    def _get_report_values(self, docids, data=None):
        if data.get('form'):
            docs = self.env['product.product'].browse(data['form'])
        else:
            docs = self.env['product.product'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'product.product',
            'docs': docs,
            'set_amount':self.set_amount,
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
