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


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    po_tripple_verify = fields.Boolean(string="Second Approval")
    po_tripple_validation_amount = fields.Float(string="Minimum Amount",
                                                help="If Total of Purchase"
                                                     " order exceeds this "
                                                     "amount, then order will "
                                                     "go into Second Approval")

    @api.model
    def set_values(self):
        ir_param = self.env['ir.config_parameter'].sudo()
        ir_param.set_param(
            'dev_purchase_order_triple_approval.po_tripple_verify',
            self.po_tripple_verify)
        ir_param.set_param(
            'dev_purchase_order_triple_approval.po_tripple_validation_amount',
            self.po_tripple_validation_amount)
        super(ResConfigSettings, self).set_values()


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ir_param = self.env['ir.config_parameter'].sudo()
        po_tripple_verify = \
            ir_param.get_param(
                'dev_purchase_order_triple_approval.po_tripple_verify')
        po_tripple_validation_amount = \
            ir_param.get_param('dev_purchase_order_triple_approval'
                               '.po_tripple_validation_amount')
        res.update(
            po_tripple_verify=bool(po_tripple_verify),
            po_tripple_validation_amount=float(po_tripple_validation_amount),
        )
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: