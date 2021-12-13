# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import date


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    @api.multi
    def action_notifi_confirm(self):
        '''
        Inherit button confirm sale order, call method send mail to personal.
        '''
        self.ensure_one()
        data = self.read()[0]
        confirm_order = super(SaleOrder, self).action_confirm()
        self.env['sea_notifications.sales_order'].sale_order_confirm(data)
        return confirm_order


class SeaNotificationSalesOrder(models.Model):
    _name = 'sea_notifications.sales_order'
    _description = 'Notification confirmation Sales Order'

    @api.multi
    def sale_order_confirm(self, data):
        mail_template = self.env.ref('sea_notifications.sea_notification_sale_order')
        objs_sale = self.env['sale.order'].search([('id', '=', data['id'])])
        if mail_template:
            mail_template.send_mail(objs_sale.id)
