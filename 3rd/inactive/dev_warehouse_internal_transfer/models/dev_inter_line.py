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


class dev_inter_line(models.Model):
    _name = 'dev.inter.line'
    
    product_id = fields.Many2one('product.product',string='Product',required="1")
    qoh = fields.Float('QOH', compute='_get_quantity_on_hand')
    send_qty = fields.Float('Transfer Qty', required="1",default=1)
    receive_qty = fields.Float('Receive Qty', required="1")
    uom_id = fields.Many2one('uom.uom',string='UOM', required="1")
    transfer_id = fields.Many2one('dev.inter.transfer',string='Inter Transfer')
    state = fields.Selection(related='transfer_id.state', string='State')
    
    
    @api.depends('product_id','uom_id')
    def _get_quantity_on_hand(self):
        for line in self:
            if line.product_id and line.uom_id:
                qoh = line.product_id.with_context(warehouse=line.transfer_id.source_warehouse_id.id).qty_available
                line.qoh = line.product_id.uom_id._compute_quantity(qoh, line.uom_id)
    
    
    @api.constrains('send_qty','receive_qty')
    def check_qty(self):
        for line in self:
            if line.send_qty < 1:
                raise ValidationError(_("Trnasfer Quantity must be greater of 0 !!!"))
            if line.receive_qty < 0:
                raise ValidationError(_("Receive Quantity must be positive !!!"))
    
    
    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            domain = {'uom_id': [('category_id', '=', self.product_id.uom_id.category_id.id)]}
            self.uom_id = self.product_id.uom_id and self.product_id.uom_id.id or False,
            return {'domain': domain}
        else:
            return {'domain': {'uom_id': []}}
        
        
        
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
