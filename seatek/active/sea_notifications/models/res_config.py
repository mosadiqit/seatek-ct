# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_notification_sale = fields.Boolean(string="Notification Sale Order comfirm", implied_group='base.group_erp_manager')
    notification_sale_id = fields.Many2one('mail.template', 'Default Template',
            domain="[('model', '=', 'sea_notifications.sales_order')]",
            default=lambda self: self.env.ref('sea_notifications.sea_notification_sale_order', False))