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


class dev_inter_transfer(models.Model):
    _name = 'dev.inter.transfer'
    _order = 'name desc'

    stage=[('draft','Draft'),
                ('transfer','Transfer'),
                ('receive','receive'),
                ('validate','Validate'),
                ('cancel','Cancel')]
                

    name = fields.Char('Name',default='/',copy=False)
    state = fields.Selection(stage,string='State',default='draft')
    date = fields.Date('Date', default = fields.Date.today())
    company_id = fields.Many2one('res.company', default=lambda self:self.env.user.company_id.id)
    user_id = fields.Many2one('res.users', default=lambda self:self.env.user.id)
    source_warehouse_id = fields.Many2one('stock.warehouse',string='Source Warehouse', required="1")
    dest_warehouse_id = fields.Many2one('stock.warehouse',string='Dest Warehouse', required="1")
    
    line_ids = fields.One2many('dev.inter.line','transfer_id',string='Transfer Products Lines ')
    move_ids = fields.Many2many('stock.move',string='Moves')
    
    transfer_user_id = fields.Many2one('res.users', string='Issue By', copy=False)
    receive_user_id = fields.Many2one('res.users', string='Receive By', copy=False)
    
    
    @api.multi
    def send_request_mail(self,template,email):
        mtp = self.env['mail.template']
        mail_tem = mtp.browse(template[1])
        if not email:
            for user in self.dest_warehouse_id.transfer_user_ids:
                if user.partner_id.email:
                    if email:
                        email = email + ','+user.partner_id.email
                    else:
                        email = user.partner_id.email
        if email:
            mail_tem.write({'email_to': email})
            mail_tem.send_mail(self.ids[0], True)
        return True
        
        
    
    def action_transfer(self):
        self.get_transit_location()
        transfer_user_ids = self.source_warehouse_id.transfer_user_ids.ids
        for line in self.line_ids:
            if line.qoh < line.send_qty:
                raise ValidationError(_("You have not enough stock of %s product !!!")% line.product_id.name)
                
        if self.env.user.id not in transfer_user_ids:
            raise ValidationError(_("You can not transfer Stock !!!"))
        else:
            self.transfer_user_id = self.env.user.id
            self.state = 'transfer'
            ir_model_data = self.env['ir.model.data']
            mail_template_id = ir_model_data.get_object_reference('dev_warehouse_internal_transfer',
                                                                  'dev_transfer_product_receive_request')
            self.send_request_mail(mail_template_id,False)  
            return True                                                    
                                                                  
    @api.multi
    def get_product_details(self, transfer):
            product_table = ''
            product_table += '''
                            <table border=1 width=80% style='margin-top: 20px;border-collapse: collapse;'>
                            <tr>
                                <td width="30%" style="background:#e0e1e2"><b>Product</b></td>
                                <th width="15%" style="background:#e0e1e2">Transfer Qty</th>
                                <th width="15%" style="background:#e0e1e2">Receiver Qty</th>
                                <th width="20%" style="background:#e0e1e2">UOM</th>
                            </tr>
                            '''
            for product in transfer.line_ids:
                td_start = '''<td>'''
                td_end = '''</td>'''
                center_s = '''<center>'''
                center_e = '''</center>'''
                td_r_start = '''<td style="text-align:right">'''
                product_table += "<tr>" + td_start + product.product_id.name + td_end + td_r_start + \
                                 str(product.send_qty) + td_end + td_r_start + \
                                 str(product.receive_qty) + td_end + td_start + center_s + \
                                 str(product.uom_id.name) + center_e + td_end + "</tr>"

            product_table += ''' </table> '''
            return product_table
            
            
        
    def action_receive(self):
        transfer_user_ids = self.dest_warehouse_id.transfer_user_ids.ids
        if self.env.user.id not in transfer_user_ids:
            raise ValidationError(_("You can not Receive Stock !!!"))
        else:
            for line in self.line_ids:
                if line.receive_qty > line.send_qty:
                    raise ValidationError(_("Receive Quantity must be less or equal transfer Quantity !!!"))
            self.receive_user_id = self.env.user.id
            self.state = 'receive'
            return True
    
    @api.multi
    def get_transit_location(self):
        if self.company_id.transit_location_id:
            return self.company_id.transit_location_id
        else:
            raise ValidationError(_('Please Select Transit Location in Inventory/Setting'))
    
    
    @api.multi
    def get_location_quantity(self,quantity,line):
        quantity = quantity
        loc_id = self.source_warehouse_id.lot_stock_id
        location_ids = self.env['stock.location'].search([('id','child_of',loc_id.id)])
        lst=[]
        for location in location_ids:
            location_qty = line.product_id.with_context(location = location.id).qty_available
            child_location_ids = self.env['stock.location'].search([('id','child_of',location.id),('id','!=',location.id)])
            child_location_qty = 0
            if child_location_ids:
                child_location_qty = line.product_id.with_context(location = child_location_ids.ids).qty_available
            location_qty = location_qty - child_location_qty
            
            if location_qty > 0:
                if quantity > 0:
                    if quantity <= location_qty:
                        lst.append({
                            'location_id':location.id,
                            'quantity':quantity,
                        })
                        quantity = 0
                    else:
                        lst.append({
                            'location_id':location.id,
                            'quantity':location_qty,
                        })
                        quantity = quantity - location_qty
        
        return lst
        
    
    @api.multi
    def create_source_move_line(self,line):
        quantity = line.uom_id._compute_quantity(line.receive_qty, line.product_id.uom_id)
        vals={
            'reference':self.name,
            'origin':self.name,
            'location_id':self.source_warehouse_id.lot_stock_id.id,
            'location_dest_id':self.get_transit_location().id,
            'product_id':line.product_id.id,
            'name':line.product_id.name or '/',
            'product_uom_qty':quantity,
            'product_uom':line.product_id.uom_id and line.product_id.uom_id.id or False,
        }
        move_id= self.env['stock.move'].create(vals)
        lst = self.get_location_quantity(quantity,line)
        move_id.reference = self.name
        for l in lst:
            if l.get('quantity'):
                ml_vals={
                    'product_id':move_id.product_id.id,
                    'location_id':l.get('location_id'),
                    'location_dest_id':move_id.location_dest_id.id,
                    'ordered_qty':l.get('quantity'),
                    'qty_done':l.get('quantity'),
                    'product_uom_id':line.product_id.uom_id and line.product_id.uom_id.id or False,
                    'move_id':move_id.id,
                }
                move_line_id = self.env['stock.move.line'].create(ml_vals)
        return move_id
        
    @api.multi
    def create_dest_move_line(self,line):
        quantity = line.uom_id._compute_quantity(line.receive_qty, line.product_id.uom_id)
        vals={
            'reference':self.name,
            'origin':self.name,
            'location_id':self.get_transit_location().id,
            'location_dest_id':self.dest_warehouse_id.lot_stock_id.id,
            'product_id':line.product_id.id,
            'name':line.product_id.name or '/',
            'product_uom_qty':quantity,
            'product_uom':line.product_id.uom_id and line.product_id.uom_id.id or False,
        }
        move_id= self.env['stock.move'].create(vals)
        move_id.reference = self.name
        ml_vals={
            'product_id':move_id.product_id.id,
            'location_id':move_id.location_id.id,
            'location_dest_id':move_id.location_dest_id.id,
            'ordered_qty':line.receive_qty,
            'qty_done':quantity,
            'product_uom_id':line.product_id.uom_id and line.product_id.uom_id.id or False,
            'move_id':move_id.id,
        }
        move_line_id = self.env['stock.move.line'].create(ml_vals)
        return move_id
    
    def action_validate(self):
        lst = []
        for line in self.line_ids:
            if line.receive_qty <= 0:
                line.receive_qty = line.send_qty
            if line.receive_qty and line.send_qty:
                move_id = self.create_source_move_line(line)
                move_id._action_confirm()
                move_id._action_done()
                lst.append(move_id.id)
                move_dest_id = self.create_dest_move_line(line)
                move_dest_id._action_confirm()
                move_dest_id._action_done()
                lst.append(move_dest_id.id)
        self.move_ids = [(6,0, lst)]
        self.state = 'validate'
        return True
                
                
        
    def action_cancel(self):
        self.state = 'cancel'
        
    def action_draft(self):
        self.state = 'draft'
        
        
    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'dev.inter.transfer') or '/'
        return super(dev_inter_transfer, self).create(vals)
        
    @api.multi
    def copy(self, default=None):
        if default is None:
            default = {}
        default['name'] = '/'
        return super(dev_inter_transfer, self).copy(default=default)
        
    @api.multi
    def action_view_moves(self):
        move_ids = self.mapped('move_ids')
        action = self.env.ref('stock.stock_move_action').read()[0]
        if len(move_ids) >= 1:
            action['domain'] = [('id', 'in', move_ids.ids)]
            action['context'] = {'group_by':'product_id'}
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
        
    @api.multi
    def unlink(self):
        for transfer in self:
            if transfer.state != 'draft':
                raise ValidationError(_("Inter transfer can delete in draft state !!!"))
        return super(dev_inter_transfer,self).unlink()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
