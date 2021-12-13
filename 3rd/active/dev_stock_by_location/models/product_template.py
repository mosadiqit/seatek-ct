# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################

from odoo import models, fields, api, exceptions, _

class product_product(models.Model):
    _inherit = 'product.product'
    
    pro_stock_by_location_lines = fields.One2many('dev.stock.location.line','product_id', string='Stock Location Lines')
    
    @api.multi
    def print_stock_location(self):
        self.load_stock_lines()
        return self.env.ref('dev_stock_by_location.report_dev_product_print_stock_location').report_action(self)
        
    
    @api.multi
    def load_stock_lines(self):
        self.pro_stock_by_location_lines.unlink()
        location_ids = self.stock_location_ids
        if not location_ids:
            location_ids = self.env['stock.location'].search([('company_id','=',self.env.user.company_id.id),('usage','=','internal')])
        line_pool = self.env['dev.stock.location.line']
        for location in location_ids:
            cc = {'location' : location.id}
            if self.stock_start_date:
                cc.update({'from_date' : self.stock_start_date})
            if self.stock_end_date:
                cc.update({'to_date' : self.stock_end_date})
            
            available_qty = self.with_context(cc).qty_available
            forecasted_qty = self.with_context(cc).virtual_available
            incoming_qty = self.with_context(cc).incoming_qty
            outgoing_qty = self.with_context(cc).outgoing_qty
            line = line_pool.create({
                'location_id':location.id,
                'available_qty':available_qty,
                'forecasted_qty':forecasted_qty,
                'incoming_qty':incoming_qty,
                'outgoing_qty':outgoing_qty,
                'product_id':self.id,
            })
            
            
    
class product_template(models.Model):
    _inherit = 'product.template'
    
    stock_start_date = fields.Date('Start Date')
    stock_end_date = fields.Date('End Date')
    stock_location_ids = fields.Many2many('stock.location', domain=[('usage','=','internal')])
    stock_by_location_lines = fields.One2many('dev.stock.location.line','product_template_id', string='Stock Location Lines')
    
    
    @api.multi
    def print_stock_location(self):
        self.load_stock_lines()
        return self.env.ref('dev_stock_by_location.report_dev_print_stock_location').report_action(self)
            
            
    
    @api.multi
    def load_stock_lines(self):
        self.stock_by_location_lines.unlink()
        location_ids = self.stock_location_ids
        if not location_ids:
            location_ids = self.env['stock.location'].search([('company_id','=',self.env.user.company_id.id),('usage','=','internal')])
        line_pool = self.env['dev.stock.location.line']
        product_ids = self.env['product.product'].search([('product_tmpl_id','=',self.id)])
        for p in product_ids:
            p.pro_stock_by_location_lines.unlink()
        for location in location_ids:
            available_qty = forecasted_qty = incoming_qty = outgoing_qty = 0
            for product in product_ids:
                cc = {'location' : location.id}
                if self.stock_start_date:
                    cc.update({'from_date' : self.stock_start_date})
                if self.stock_end_date:
                    cc.update({'to_date' : self.stock_end_date})
                
                available_qty += product.with_context(cc).qty_available
                forecasted_qty += product.with_context(cc).virtual_available
                incoming_qty += product.with_context(cc).incoming_qty
                outgoing_qty += product.with_context(cc).outgoing_qty
                
                a_qty = product.with_context(cc).qty_available
                f_qty = product.with_context(cc).virtual_available
                i_qty = product.with_context(cc).incoming_qty
                o_qty = product.with_context(cc).outgoing_qty
                
                
                line_pool.create({
                    'location_id':location.id,
                    'available_qty':a_qty,
                    'forecasted_qty':f_qty,
                    'incoming_qty':i_qty,
                    'outgoing_qty':o_qty,
                    'product_id':product.id,
                })
            
            
                    
            line_pool.create({
                'location_id':location.id,
                'available_qty':available_qty,
                'forecasted_qty':forecasted_qty,
                'incoming_qty':incoming_qty,
                'outgoing_qty':outgoing_qty,
                'product_template_id':self.id,
            })
            
    
class dev_stock_location_line(models.Model):
    _name ='dev.stock.location.line'
    
    location_id = fields.Many2one('stock.location', string='Location', required="1")
    available_qty = fields.Float('Available Qty')
    forecasted_qty = fields.Float('Forecasted Qty')
    incoming_qty = fields.Float('Incoming Qty')
    outgoing_qty = fields.Float('Outgoing Qty')
    product_template_id = fields.Many2one('product.template', string='Product')
    product_id = fields.Many2one('product.product', string='Product')
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
