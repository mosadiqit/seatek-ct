# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SeaMenuBase(models.Model):
    _name = 'sea_menu_base.dash'
    _description = 'Opensea Menu'

    company_id = fields.Many2one('res.company', string='Company')
    logo = fields.Binary(related='company_id.logo', string='Logo')
