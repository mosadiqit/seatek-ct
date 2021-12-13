# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class ResCompany(models.Model):
    _inherit = "res.company"

    support_project_id = fields.Many2one('project.project', string='Support Project')
    support_invoice_product_id = fields.Many2one('product.product', string='Support Invoice Product')
    support_timesheet_invoice_product_id = fields.Many2one('product.product', string='Support Timesheet Invoice Product')


class SupportConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    support_project_id = fields.Many2one('project.project', string='Support Project')
    support_invoice_product_id = fields.Many2one('product.product', string='Support Invoice Product')
    support_timesheet_invoice_product_id = fields.Many2one('product.product', string='Support Timesheet Invoice Product')

    @api.model
    def get_values(self):
        res = super(SupportConfigSettings, self).get_values()
        res.update(
            support_project_id=self.env.user.company_id.support_project_id and self.env.user.company_id.support_project_id.id or False,
            support_invoice_product_id=self.env.user.company_id.support_invoice_product_id and self.env.user.company_id.support_invoice_product_id.id or False,
            support_timesheet_invoice_product_id=self.env.user.company_id.support_timesheet_invoice_product_id and self.env.user.company_id.support_timesheet_invoice_product_id.id or False
        )
        return res

    @api.multi
    def set_values(self):
        super(SupportConfigSettings, self).set_values()
        self.ensure_one()
        if not self.env.user._is_admin():
            raise AccessError(_("Only administrators can change the settings"))

        self.env.user.company_id.support_project_id = self.support_project_id
        self.env.user.company_id.support_invoice_product_id = self.support_invoice_product_id
        self.env.user.company_id.support_timesheet_invoice_product_id = self.support_timesheet_invoice_product_id

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
