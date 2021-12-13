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

class report_inter_transfer(models.AbstractModel): 
    _name = 'report.dev_warehouse_internal_transfer.re_dev_inter_tran'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['dev.inter.transfer'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'dev.inter.transfer',
            'docs': docs,
        }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
