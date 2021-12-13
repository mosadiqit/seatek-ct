# -*- coding: utf-8 -*-
from datetime import timedelta

import pytz

from odoo import fields, models, tools, api
import odoo.addons.decimal_precision as dp
from odoo.addons.mail.models.mail_template import format_tz
from odoo.fields import Datetime


class InventoryReport(models.Model):
    _name = 'seatek.inventory.report'
    _description = 'Báo cáo xuất nhập tồn'

    name = fields.Char('Tên', default='Báo cáo xuất nhập tồn')

    date_from = fields.Datetime('Từ ngày', default=fields.Datetime.today())
    date_to = fields.Datetime('Đến ngày', default=fields.Datetime.today())
    type_get_value = fields.Selection([
            ('product', 'Giá trên sản phẩm'),
            ('stock', 'Quy trình kho'),
            ('account', 'Bút toán')], 'Lấy giá trị theo', default='product')
    value = fields.Float('Giá trị kho', digits=dp.get_precision('Product Price'), readonly=True)

    @api.model
    def get_location_default(self):
        return self.env['stock.location'].search([('id', '=', 21)]).ids

    @api.model
    def get_product_default(self):
        return self.env['product.product'].search([('id', '=', 25)]).ids

    location_ids = fields.Many2many('stock.location',
                                    'seatek_inventory_report_location_rel',
                                    'report_id',
                                    'location_id',
                                    'Địa điểm kho',
                                    domain=[('usage', 'in', ('internal', 'transit'))],
                                    default=get_location_default)

    categ_ids = fields.Many2many('product.category', 'vio_inventory_report_pc_rel', 'report_id', 'categ_id',
                                 'Nhóm sản phẩm')
    product_ids = fields.Many2many('product.product', 'vio_inventory_report_product_rel', 'report_id', 'product',
                                   'Sản phẩm', default=get_product_default)

    user_id = fields.Many2one('res.users')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id)

    display_product = fields.Boolean("Ẩn sản phẩm bằng 0", default=False)
    inventory_report_line_ids = fields.One2many('seatek.inventory.report.line', 'inventory_report_id', 'Chi tiết')
    inventory_report_line_ids_hide_display_product = fields.One2many('seatek.inventory.report.line', 'inventory_report_id', 'Chi tiết',
                                                                    domain=['|', '|', '|',
                                                                    ('stock_out', '!=', 0),
                                                                    ('stock_opening', '!=', 0),
                                                                    ('stock_closing', '!=', 0),
                                                                    ('stock_in', '!=', 0)])

    @api.onchange('categ_ids')
    def _categ_onchange(self):
        res = {}
        list_categ_ids = []
        categ = self.categ_ids
        if len(categ) > 1:
            for cate in categ:
                list_categ_ids.append(cate.id)
            res['domain'] = {'product_ids': [('categ_id', 'in', list_categ_ids)]}
        else:
            res['domain'] = {'product_ids': [('categ_id', '=', categ.id)]}
        return res

    def action_get_data_inventory_report_line(self):
        self.inventory_report_line_ids.unlink()

        LineObj = self.env['seatek.inventory.report.line']
        ProductObj = self.env['product.product']

        domain_product = []
        if self.categ_ids:
            domain_product.append(('categ_id', 'in', self.categ_ids.ids))
        if self.product_ids:
            domain_product.append(('id', 'in', self.product_ids.ids))
        products = ProductObj.search([('type', 'in', ('product', 'consu'))] + domain_product)

        # """đầu kỳ và tồn của tất cả các loại sản phẩm consu bằng 0"""
        products_consu = ProductObj.search([('type', '=', 'consu')])

        location_ids = self.location_ids.ids
        if not location_ids:
            location_ids = self.env['stock.location'].search([('usage', 'in', ('internal', 'transit'))]).ids
        value = 0

        domain_date = []
        
        if self.date_to:
            dt_to = Datetime.context_timestamp(self, self.date_to).replace(minute=59, hour=23, second=59)
            dt_to = dt_to.astimezone(pytz.utc)
            self.date_to = dt_to.replace(tzinfo=None)
            domain_date.append(('date', '<=', dt_to))
        if self.date_from:
            dt_from = Datetime.context_timestamp(self, self.date_from).replace(hour=0, minute=0, second=0)
            self.date_from = dt_from.replace(tzinfo=None)
            domain_date.append(('date', '>=', dt_from)) 

        for product in products:
            for location in location_ids:
                domain_in = [('location_id', '!=', location), ('location_dest_id', '=', location)]
                domain_out = [('location_id', '=', location), ('location_dest_id', '!=', location)]

                move_in_ids = self.env['stock.move.line'].read_group(
                    [('state', '=', 'done')] + domain_in + domain_date,
                    fields=['product_id', 'qty_done'], groupby=['product_id'])

                move_out_ids = self.env['stock.move.line'].read_group(
                    [('state', '=', 'done')] + domain_out + domain_date,
                    fields=['product_id', 'qty_done'], groupby=['product_id'])

                qty_in_of_product = list(filter(lambda item: item["product_id"][0] == product.id, move_in_ids))
                qty_out_of_product = list(filter(lambda item: item["product_id"][0] == product.id, move_out_ids))

                if len(qty_in_of_product) == 0:
                    qty_in_of_product = 0
                else:
                    qty_in_of_product = qty_in_of_product[0]['qty_done']

                if len(qty_out_of_product) == 0:
                    qty_out_of_product = 0
                else:
                    qty_out_of_product = qty_out_of_product[0]['qty_done']

                qty_closing = product.with_context(location=location, to_date=self.date_to).qty_available
                qty_opening = qty_closing + qty_out_of_product - qty_in_of_product
                line = LineObj.search([('inventory_report_id', '=', self.id), ('product_id', '=', product.id),
                                    ('location_id', '=', location)], limit=1)
                value_stock_opening = product.standard_price * qty_opening
                value_stock_closing = product.standard_price * qty_closing
                value_stock_in = product.standard_price * qty_in_of_product
                value_stock_out = product.standard_price * qty_out_of_product
                if not line:
                    line = LineObj.create({
                        'inventory_report_id': self.id,
                        'product_id': product.id,
                        'uom_id': product.uom_id.id,
                        'stock_opening': qty_opening,
                        'stock_in':qty_in_of_product,
                        'stock_out':qty_out_of_product,
                        'value_stock_in': value_stock_in,
                        'value_stock_out': value_stock_out,
                        'stock_closing': qty_closing,
                        'location_id': location,
                        'value_stock_opening': value_stock_opening,
                        'value_stock_closing': value_stock_closing
                    })
                else:
                    line.write({
                        'stock_in':qty_in_of_product,
                        'stock_out':qty_out_of_product,
                        'value_stock_in': value_stock_in,
                        'value_stock_out': value_stock_out,
                        'stock_opening': qty_opening,
                        'stock_closing': qty_closing,
                    })
                for consu in products_consu:
                    if consu == product:
                        if not line:
                            line = LineObj.create({
                                'inventory_report_id': self.id,
                                'product_id': product.id,
                                'uom_id': product.uom_id.id,
                                'location_id': location,
                                'stock_opening': 0,
                                'stock_closing': 0,
                            })
                        else:
                            line.write({
                                'stock_opening': 0,
                                'stock_closing': 0,
                            })
                value += value_stock_closing

                self.value = value

    def action_report_excel(self):
        return self.env.ref('seatek_stock_report_xnt._report_excel').report_action(self)


class InventoryReportLine(models.Model):
    _name = 'seatek.inventory.report.line'
    _description = 'Chi tiết xuất nhập tồn tổng quát'

    inventory_report_id = fields.Many2one('seatek.inventory.report', 'Inventory report id', ondelete='cascade')
    product_id = fields.Many2one('product.product', 'Sản phẩm')
    uom_id = fields.Many2one('uom.uom', 'Đơn vị')
    stock_opening = fields.Float('Tồn đầu kỳ', digits=dp.get_precision('Product Unit of Measure'))
    stock_in = fields.Float('Nhập trong kỳ', digits=dp.get_precision('Product Unit of Measure'))
    stock_out = fields.Float('Xuất trong kỳ', digits=dp.get_precision('Product Unit of Measure'))
    stock_closing = fields.Float('Tồn cuối kỳ', digits=dp.get_precision('Product Unit of Measure'))
    location_id = fields.Many2one('stock.location',
                                  'Địa điểm kho',
                                  domain=[('usage', 'in', ('internal', 'transit'))])

    value_stock_opening = fields.Float('Giá trị kho đầu kì', digits=(16, 0))
    value_stock_in = fields.Float('Giá trị nhập', digits=(16, 0))
    value_stock_out = fields.Float('Giá trị xuất', digits=(16, 0))
    value_stock_closing = fields.Float('Giá trị kho cuối kì', digits=(16, 0))
