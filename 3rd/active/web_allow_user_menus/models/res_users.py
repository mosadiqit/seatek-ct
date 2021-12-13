# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class Users(models.Model):
    _inherit = "res.users"

    @api.onchange('sub_menu_id')
    def onchange_sub_menu_id(self):
        if self.sub_menu_id:
            menu_ids = self.env['ir.ui.menu'].search([('id', 'parent_of', self.sub_menu_id.id)])
            if menu_ids:
                self.menu_ids += menu_ids
                self.sub_menu_id = False

    sub_menu_id = fields.Many2one('ir.ui.menu', string="Add Submenu")
    menu_ids = fields.Many2many('ir.ui.menu', string="Menus")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
