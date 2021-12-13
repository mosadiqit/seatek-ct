# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # company_id = fields.Many2one('res.company', string='Company', required=False,
    #                              default=lambda self: self.env.user.company_id)

    report_pegasusorder_document = fields.Many2one(related="company_id.purchase_order_report", readonly=False,
                                         domain=lambda self: self._domain_purchase_order_report()
                                         )

    def _domain_purchase_order_report(self):
        domain = [('name', 'in',
                   [
                       'report_pegasusorder_document',
                   ]
                   )]
        return domain

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        # res.update(
        #     my_template_id=self._default()
        # )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        # print(self.my_template_id.id)
        # self.company_id.write({'my_template_id': self.my_template_id.id})

    @api.model
    def create(self, values):
        return super(ResConfigSettings, self).create(values)
