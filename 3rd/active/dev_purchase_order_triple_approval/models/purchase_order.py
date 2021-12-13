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


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection([('draft', 'RFQ'),
                              ('sent', 'RFQ Sent'),
                              ('to approve', 'To Approve'),
                              ('second approval', 'To Second Approval'),
                              ('purchase', 'Purchase Order'),
                              ('done', 'Locked'),
                              ('cancel', 'Cancelled')],
                             string='Status', readonly=True,
                             index=True, copy=False, default='draft',
                             track_visibility='onchange')

    @api.multi
    def _make_url(self, record_id, model_name, menu_id, action_id):
        ir_param = self.env['ir.config_parameter'].sudo()
        base_url = ir_param.get_param('web.base.url')
        if base_url:
            base_url += \
                '/web?#id=%s&action=%s&model=%s&view_type=form&menu_id=%s' \
                % (record_id, action_id, model_name, menu_id)
        return base_url


    @api.multi
    def purchase_details(self, order):
        ref = ''
        supplier = ''
        amount = ''
        if order.name:
            ref = str(order.name)
        if order.partner_id.name:
            supplier = str(order.partner_id.name)
        if order.amount_total:
            amount = str(order.amount_total)
        table = ''''''
        table += \
            '''<table width="40%" border='1' style='table-layout: fixed;'>'''
        table += '''
                    <tr>
                        <th colspan='2'><center>Order Details</center></th>
                    </tr>
                    <tr>
                        <td width='10%'><b>Purchase Order</b></td>
                        <td width='30%'>''' + ref + '''</td>
                    </tr>
                    <tr style='word-wrap: break-word;'>
                        <td td width='10%'><b>Supplier</b></td>
                        <td td width='30%'>''' + supplier + '''</td>
                    </tr>
                    <tr>
                        <td td width='10%'><b>Amount</b></td>
                        <td td width='30%'>''' + amount + '''</td>
                    </tr>'''
        table += '''</table>'''
        return table or ''


    @api.multi
    def send_approval_email(self, authorized_group, order):
        authorized_users = self.env['res.users'].search(
            [('groups_id', '=', authorized_group.id)])
        menu_id = order.env.ref('purchase.menu_purchase_form_action').id
        action_id = order.env.ref('purchase.purchase_form_action').id
        purchase_url = order._make_url(order.id, order._name,
                                       menu_id, action_id)
        purchase_table = order.purchase_details(order)
        if authorized_users:
            for au_user in authorized_users:
                email_body = ''' <span style='font-style: 16px;font-weight:\
                bold;'>Dear, <b>%s</b></span>''' % (au_user.name) + '''<br/>\
                <br/>''' + ''' <span style='font-style: 14px;'> A Purchase \
                Order from <span style='font-weight: bold;'>%s</span> is \
                awaiting for your Approval</span>''' % (order.env.user.name)+'''\
                <br/><br/>''' + purchase_table + '''<span style='font-style: \
                14px;'><br/><br/>Please, access order form below button</span> \
                <div style="margin-top:40px;"> <a href="'''+ purchase_url +'''"\
                style="background-color:#1abc9c; padding: 20px;text-decoration:\
                 none;color: #fff; border-radius: 5px; font-size:16px;"\
                 class="o_default_snippet_text">View Purchase Order</a>\
                 </div><br/><br/>'''
                email_id = order.env['mail.mail'].\
                    create({'subject': 'Purchase Order is Waiting for Approval',
                            'email_from': order.env.user.partner_id.email,
                            'email_to': au_user.partner_id.email,
                            'message_type': 'email',
                            'body_html': email_body})
                email_id.send()

    @api.multi
    def button_approve(self, force=False):
        for order in self:
            ir_param = self.env['ir.config_parameter'].sudo()
            is_double_enabled = False
            if order.company_id.po_double_validation == 'two_step':
                is_double_enabled = True
            if is_double_enabled:
                is_triple_enabled = bool(ir_param.get_param(
                    'dev_purchase_order_triple_approval.po_tripple_verify'))
                triple_validation_amount = \
                    float(ir_param.get_param('dev_purchase_order_triple_approval.'
                                       'po_tripple_validation_amount'))
                approval_group = 'dev_purchase_order_triple_approval.' \
                                 'triple_verification_po_right'
                triple_approval_rights =\
                    order.env.user.has_group(str(approval_group))
                if is_triple_enabled:
                    if order.amount_total < triple_validation_amount or\
                            triple_approval_rights:
                        return super(PurchaseOrder, self).button_approve(force=force)
                    else:
                        authorized_group = order.env.ref(str(approval_group))
                        order.send_approval_email(authorized_group, order)
                        order.write({'state': 'second approval'})
                else:
                    return super(PurchaseOrder, self).button_approve(force=force)
            else:
                return super(PurchaseOrder, self).button_approve(force=force)

    @api.multi
    def confirm_purchase_order(self):
        for order in self:
            return super(PurchaseOrder, self).button_approve(force=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: