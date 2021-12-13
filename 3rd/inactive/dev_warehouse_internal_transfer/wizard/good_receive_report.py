 # -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Devintelle Solutions (<http://devintellecs.com/>).
#
##############################################################################

from odoo import api, fields, models, _
from datetime import datetime
import calendar

class goods_receive_report(models.TransientModel):
    _name = "goods.receive.report"
    
    @api.model
    def _get_from_date(self):
        date = datetime.now()
        month = date.month
        if date.month < 10:
            month = '0'+str(date.month)
        date = str(date.year)+'-'+str(month)+'-01'
        return date
        
    @api.model
    def _get_to_date(self):
        date = datetime.now()
        m_range = calendar.monthrange(date.year,date.month)
        month = date.month
        if date.month < 10:
            month = '0'+str(date.month)
        date = str(date.year)+'-'+str(month)+'-'+str(m_range[1])
        return date
    
    from_date = fields.Date('From Date', required="1", default=_get_from_date)
    to_date = fields.Date('To Date', required="1", default=_get_to_date)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self:self.env.user.company_id)
    warehouse_id =fields.Many2one('stock.warehouse', string='Warehouse')
    
    
    
    
    @api.multi
    def print_pdf(self):
        data={}
        data['form'] = self.read()[0]
        return self.env.ref('dev_warehouse_internal_transfer.print_goods_receive_report').report_action(self, data=None)
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
