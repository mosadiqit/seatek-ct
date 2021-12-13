# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################

from odoo import models, fields, api
import itertools
from operator import itemgetter
import operator

class report_goods_receive_report(models.AbstractModel): 
    _name = 'report.dev_warehouse_internal_transfer.goods_receive_rep_temp'

    @api.multi
    def get_lines(self,obj):
        inter_transfer_pool = self.env['dev.inter.transfer']
        if obj.from_date and obj.to_date:
            transfer_ids = inter_transfer_pool.search([('dest_warehouse_id','=',obj.warehouse_id.id),
                                                   ('date','>=',obj.from_date),
                                                   ('date','<=',obj.to_date),
                                                   ('state','=','validate')])
            lst =[]
            for tra in transfer_ids:
                for transfer in tra.line_ids:
                    qty = transfer.uom_id._compute_quantity(transfer.receive_qty, transfer.product_id.uom_id)
                    lst.append({
                        'product':transfer.product_id.name or '',
                        'qty':qty,
                        'uom_id':transfer.product_id and transfer.product_id.uom_id and transfer.product_id.uom_id.name or '',
                    })
            
            if lst:
                n_lines=sorted(lst,key=itemgetter('product'))
                groups = itertools.groupby(n_lines, key=operator.itemgetter('product'))
                lst = [{'product':k,'values':[x for x in v]} for k, v in groups]
            
        return lst
            
            
    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['goods.receive.report'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'goods.receive.report',
            'docs': docs,
            'get_lines':self.get_lines,
        }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
