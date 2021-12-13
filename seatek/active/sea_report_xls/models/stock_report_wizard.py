# -*- coding: utf-8 -*-
import pytz, datetime
from pytz import timezone
from datetime import timedelta
from odoo import models, fields, api, exceptions, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import ValidationError


class WizardStockReport(models.TransientModel):
    _name = 'sea_report_xls.stock_report.wizard'

    @api.onchange('location_ids')
    def _default_picking_type(self):
        self.picking_type_ids = [(5, 0, 0)]
        if self.location_ids:
            domain_ids = []
            location_src = self.env['stock.picking.type'].search([('default_location_src_id', 'in', self.location_ids.ids)])
            domain_ids += location_src.ids
            location_dest = self.env['stock.picking.type'].search([('default_location_dest_id', 'in', self.location_ids.ids)])
            domain_ids += location_dest.ids
            return {'domain': {'picking_type_ids': [('id', 'in', domain_ids)]}}
        else:
            return {'domain': {'picking_type_ids': []}}

    
    @api.constrains('date_from', 'date_to')
    def _constrain_dates(self):
        for rec in self:
            if rec.date_from > rec.date_to:
                raise ValidationError(_('Date From must be greater than date To!'))

    date_from = fields.Date(string='Date From', default=fields.Date.today() - timedelta(days=1))
    date_to = fields.Date(string='Date To', default=fields.Date.today())
    product_ids = fields.Many2many('product.product', 'report_stock_move_xls_product_rel', 'wizard_id', 'warehouse_id', 'Product')
    location_ids = fields.Many2many('stock.location', 'report_stock_move_xls_location_rel', 'wizard_id', 'warehouse_id', 'Location', domain=[('usage', 'in', ('internal', 'transit'))])
    picking_type_ids = fields.Many2many('stock.picking.type', 'report_stock_move_xls_picking_type_rel', 'wizard_id', 'warehouse_id', 'Picking Type')
    warehouse_ids = fields.Many2many('stock.warehouse', 'report_stock_move_xls_warehosue_rel', 'wizard_id', 'warehouse_id', 'Warehouse')


    @api.model
    def conver_timezone(self, var):
        user = self.env["res.users"].browse(self._uid)
        tz = timezone(user.tz)
        c_time = datetime.datetime.now(tz)
        hour_tz = int(str(c_time)[-5:][:2])
        min_tz = int(str(c_time)[-5:][3:])
        sign = str(c_time)[-6][:1]
        if sign == '+':
            var_time = datetime.datetime.strptime(str(var), DEFAULT_SERVER_DATETIME_FORMAT) - timedelta(hours=hour_tz, minutes=min_tz)
        else:
            var_time = datetime.datetime.strptime(str(var), DEFAULT_SERVER_DATETIME_FORMAT) + timedelta(hours=hour_tz, minutes=min_tz)
        return str(var_time)

    @api.multi
    def find_objs(self):
        date_from = datetime.datetime(year=self.date_from.year, month=self.date_from.month, day=self.date_from.day, hour=0, minute=0, second=0)
        date_to = datetime.datetime(year=self.date_to.year, month=self.date_to.month, day=self.date_to.day, hour=23, minute=59, second=59)
        search_objs = [('date', '>=', self.conver_timezone(date_from)), ('date', '<=', self.conver_timezone(date_to)), ('state', '=', 'done')]
        search_product = ('product_id.id', 'in', self.product_ids.ids)
        search_picking_type = ('picking_type_id.id', 'in', self.picking_type_ids.ids)
        search_location_in = ('location_dest_id.id', 'in', self.location_ids.ids)
        search_location_not_in = ('location_id.id', 'not in', self.location_ids.ids)
        search_location_out = ('location_dest_id.id', 'not in', self.location_ids.ids)
        search_location_not_out =('location_id.id', 'in', self.location_ids.ids)
        if self.product_ids:
            search_objs.append(search_product)
        if self.picking_type_ids:
            search_objs.append(search_picking_type)
        if self.location_ids:
            search_in = [search_location_in, search_location_not_in]
            search_in += search_objs
            search_out = [search_location_out, search_location_not_out]
            search_out += search_objs
            objs_search = self.env['stock.move'].search(search_in) + self.env['stock.move'].search(search_out)
        else:
            objs_search = self.env['stock.move'].search(search_objs)
        if not objs_search:
                raise ValidationError(_('The period choose has no data to report! Please select a different time period.'))
        else:
            return objs_search

    @api.multi
    def view_report(self):
        self.ensure_one()
        if not self.env.user.tz:
            raise ValidationError(_('Please contact Administrator to configure your time zone!!!'))
        else:
            data = self.read()[0]
            objs_stock_move = self.find_objs()
            datas = {
                'ids': objs_stock_move.ids,
                'model': 'stock.move',
                'form': data,
                'product': self.product_ids.ids,
                'location': self.location_ids.ids,
                'picking_type': self.picking_type_ids.ids,
            }
            return self.env['ir.actions.report'].search(
                [('report_name', '=', 'sea_report_xls.stock_report_xls'),
                ('report_type', '=', 'xlsx')],
                limit=1).report_action(self, data=datas)
