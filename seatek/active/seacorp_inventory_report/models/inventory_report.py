# -*- coding: utf-8 -*-
from odoo import fields, models, tools, api
import odoo.addons.decimal_precision as dp
from odoo.tools import float_is_zero
from dateutil.relativedelta import relativedelta
from odoo.tools import date_utils, float_utils
import pytz


DATE_RANGE_TYPES = [
    ('today', 'Hôm nay'),
    ('yesterday', 'Hôm qua'),
    ('this_week', 'Tuần này'),
    ('last_week', 'Tuần trước'),
    ('this_month', 'Tháng này'),
    ('last_month', 'Tháng trước'),
    ('this_year', 'Năm nay'),
    ('last_year', 'Năm trước'),
]

def compute_date_domain(date_range_type):
    start = False
    end = False
    today = fields.Date.today()
    if date_range_type == 'today':
        start = today
        end = today
    elif date_range_type == 'yesterday':
        start = today + relativedelta(days=-1)
        end = today + relativedelta(days=-1)
    elif date_range_type == 'this_week':
        start = date_utils.start_of(today, 'week')
        end = start + relativedelta(days=6)
    elif date_range_type == 'last_week':
        start_this_week = date_utils.start_of(today, 'week')
        start = start_this_week - relativedelta(days=7)
        end = start_this_week + relativedelta(days=-1)
    elif date_range_type == 'this_month':
        start = date_utils.start_of(today, 'month')
        end = start + relativedelta(months=1, days=-1)
    elif date_range_type == 'last_month':
        start_this_month = date_utils.start_of(today, 'month')
        start = start_this_month - relativedelta(months=1)
        end = start_this_month + relativedelta(days=-1)
    elif date_range_type == 'this_year':
        start = date_utils.start_of(today, 'year')
        end = start + relativedelta(years=1, days=-1)
    elif date_range_type == 'last_year':
        start_this_year = date_utils.start_of(today, 'year')
        start = start_this_year - relativedelta(years=1)
        end = start_this_year + relativedelta(days=-1)
    return start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')


class InventoryReport(models.Model):
    _name = 'vio.inventory.report'
    _description = 'Báo cáo xuất nhập tồn'

    name = fields.Char('Tên', default='Báo cáo xuất nhập tồn')
    inventory_report_line_ids = fields.One2many('vio.inventory.report.line', 'inventory_report_id', 'Chi tiết')

    date_range_type = fields.Selection(selection=DATE_RANGE_TYPES, string='Chu kỳ')

    date_from = fields.Date('Từ ngày', required=False, default=fields.Date.today)
    date_to = fields.Date('Đến ngày', default=fields.Date.today)
    type_get_value = fields.Selection([
            ('product', 'Giá trên sản phẩm'),
            ('stock', 'Quy trình kho'),
            ('account', 'Bút toán')], 'Lấy giá trị theo', default='product')
    value = fields.Float('Giá trị kho', digits=dp.get_precision('Product Price'), readonly=True)
    location_ids = fields.Many2many('stock.location', 'vio_inventory_report_location_rel', 'report_id', 'location_id', 'Địa điểm kho', domain=[('usage', 'in', ('internal', 'transit'))])

    user_id = fields.Many2one('res.users')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id)

    categ_ids = fields.Many2many('product.category', 'vio_inventory_report_pc_rel', 'report_id', 'categ_id', 'Nhóm sản phẩm')
    product_ids = fields.Many2many('product.product', 'vio_inventory_report_product_rel', 'report_id', 'product', 'Sản phẩm')

    hide_zero_line = fields.Boolean('Ẩn dòng không có phát sinh')

    @api.onchange('date_range_type')
    def onchange_date_range_type(self):
        if self.date_range_type:
            self.date_from, self.date_to = compute_date_domain(self.date_range_type)

    def delete_zero_line(self):
        for line in self.inventory_report_line_ids:
            if not float_is_zero(line.stock_opening, precision_rounding=2):
                continue
            if not float_is_zero(line.stock_in, precision_rounding=2):
                continue
            if not float_is_zero(line.stock_out, precision_rounding=2):
                continue
            if not float_is_zero(line.stock_closing, precision_rounding=2):
                continue
            line.unlink()

    def action_get_data_inventory_report_line(self):
        self.inventory_report_line_ids.unlink()

        LineObj = self.env['vio.inventory.report.line']
        ProductObj = self.env['product.product']
        LocationObj = self.env['stock.location']

        domain_product = []
        if self.categ_ids:
            domain_product.append(('categ_id', 'in', self.categ_ids.ids))
        if self.product_ids:
            domain_product.append(('id', 'in', self.product_ids.ids))
        products = ProductObj.search([('type', 'in', ('product', 'consu'))] + domain_product)

        location_ids = self.location_ids.ids
        if not location_ids:
            location_ids = LocationObj.search([('usage', 'in', ('internal', 'transit'))]).ids
        value = 0

        tzinfo = pytz.timezone(self._context.get('tz', 'utc') or 'utc')

        domain_date = []

        date_to = tzinfo.localize(fields.Datetime.from_string(str(fields.Date.today()))).astimezone(pytz.UTC)
        date_from = tzinfo.localize(fields.Datetime.from_string(str(fields.Date.today()))).astimezone(pytz.UTC)

        if self.date_to:
            date_to = tzinfo.localize(fields.Datetime.from_string(str(self.date_to))).astimezone(pytz.UTC)
            date_to += relativedelta(days=1, seconds=-1)
            date_to = str(date_to)
            domain_date.append(('date', '<=', date_to))
        if self.date_from:
            date_from = tzinfo.localize(fields.Datetime.from_string(str(self.date_from))).astimezone(pytz.UTC)
            domain_date.append(('date', '>=', str(date_from)))
            date_from += relativedelta(seconds=-1)
            date_from = str(date_from)

        domain_in = [('location_id', 'not in', location_ids), ('location_dest_id', 'in', location_ids)]
        domain_out = [('location_id', 'in', location_ids), ('location_dest_id', 'not in', location_ids)]

        for product in products:
            qty_opening = product.with_context(location=location_ids, to_date=date_from).qty_available
            qty_closing = product.with_context(location=location_ids, to_date=date_to).qty_available
            line = LineObj.search([('inventory_report_id', '=', self.id), ('product_id', '=', product.id)], limit=1)
            line_val = {
                'inventory_report_id': self.id,
                'product_id': product.id,
                'uom_id': product.uom_id.id,
                'stock_opening': qty_opening,
                'stock_closing': qty_closing,
                'stock_adj_in': 0,
                'stock_in_internal': 0,
                'stock_purchase': 0,
                'stock_refund': 0,
                'stock_adj_out': 0,
                'stock_ount_internal': 0,
                'stock_refund_supplier': 0,
                'stock_sale': 0,
                'stock_mo': 0,
                'stock_to_mo': 0,
            }

            move_in_ids = self.env['stock.move.line'].read_group(
                [('state', '=', 'done'), ('product_id', '=', product.id)] + domain_in + domain_date,
                ['qty_done'], ['location_id'])

            for move_val in move_in_ids:
                location = LocationObj.browse(move_val['location_id'][0])
                qty_done = move_val['qty_done']
                if location.usage == 'inventory':
                    line_val['stock_adj_in'] += qty_done
                elif location.usage in ('internal', 'transit'):
                    line_val['stock_in_internal'] += qty_done
                elif location.usage == 'supplier':
                    line_val['stock_purchase'] += qty_done
                elif location.usage == 'customer':
                    line_val['stock_refund'] += qty_done
                elif location.usage == 'production':
                    line_val['stock_mo'] += qty_done
                else:
                    line_val['stock_in_other'] += qty_done

            move_out_ids = self.env['stock.move.line'].read_group(
                [('state', '=', 'done'), ('product_id', '=', product.id)] + domain_out + domain_date,
                ['qty_done'], ['location_dest_id'])

            for move_val in move_out_ids:
                location = LocationObj.browse(move_val['location_dest_id'][0])
                qty_done = move_val['qty_done']
                if location.usage == 'inventory':
                    line_val['stock_adj_out'] += qty_done
                elif location.usage in ('internal', 'transit'):
                    line_val['stock_ount_internal'] += qty_done
                elif location.usage == 'supplier':
                    line_val['stock_refund_supplier'] += qty_done
                elif location.usage == 'customer':
                    line_val['stock_sale'] += qty_done
                elif location.usage == 'production':
                    line_val['stock_to_mo'] += qty_done
                else:
                    line_val['stock_out_other'] += qty_done

            if not line:
                line = LineObj.create(line_val)
            else:
                line.write(line_val)

            value += product.standard_price * qty_closing
        if self.hide_zero_line:
            self.delete_zero_line()
        self.value = value

    def action_open_detail(self):
        action = self.env.ref('seacorp_inventory_report.action_inventory_report_line_view').read()[0]
        action['domain'] = [('inventory_report_id', 'in', self.ids)]
        return action

class InventoryReportLine(models.Model):
    _name = 'vio.inventory.report.line'
    _description = 'Chi tiết xuất nhập tồn'

    @api.depends('stock_adj_in', 'stock_in_internal', 'stock_purchase', 'stock_refund', 'stock_mo', 'stock_in_other')
    def compute_stock_in(self):
        for record in self:
            record.stock_in = record.stock_adj_in + record.stock_in_internal + record.stock_purchase + record.stock_refund + record.stock_mo + record.stock_in_other

    @api.depends('stock_sale', 'stock_adj_out', 'stock_ount_internal', 'stock_refund_supplier', 'stock_to_mo', 'stock_out_other')
    def compute_stock_out(self):
        for record in self:
            record.stock_out = record.stock_sale + record.stock_adj_out + record.stock_ount_internal + record.stock_refund_supplier + record.stock_to_mo + record.stock_out_other

    inventory_report_id = fields.Many2one('vio.inventory.report', 'Inventory report id', ondelete='cascade')
    product_id = fields.Many2one('product.product', 'Sản phẩm')
    uom_id = fields.Many2one('uom.uom', 'Đơn vị')
    stock_opening = fields.Float('Tồn đầu kỳ', digits=dp.get_precision('Product Unit of Measure'))

    stock_adj_in = fields.Float('Điều chỉnh tăng', digits=dp.get_precision('Product Unit of Measure'))
    stock_in_internal = fields.Float('Nhập nội bộ', digits=dp.get_precision('Product Unit of Measure'))
    stock_purchase = fields.Float('Mua', digits=dp.get_precision('Product Unit of Measure'))
    stock_refund = fields.Float('Khách trả hàng', digits=dp.get_precision('Product Unit of Measure'))
    stock_mo = fields.Float('Sản xuất', digits=dp.get_precision('Product Unit of Measure'))
    stock_in_other = fields.Float('Nhập khác', digits=dp.get_precision('Product Unit of Measure'))
    stock_in = fields.Float('Tổng nhập', compute='compute_stock_in', store=True, digits=dp.get_precision('Product Unit of Measure'))

    stock_sale = fields.Float('Bán', digits=dp.get_precision('Product Unit of Measure'))
    stock_adj_out = fields.Float('Điều chỉnh giảm', digits=dp.get_precision('Product Unit of Measure'))
    stock_ount_internal = fields.Float('Xuất nội bộ', digits=dp.get_precision('Product Unit of Measure'))
    stock_refund_supplier = fields.Float('Trả hàng NCC', digits=dp.get_precision('Product Unit of Measure'))
    stock_to_mo = fields.Float('NVL SX', digits=dp.get_precision('Product Unit of Measure'))
    stock_out_other = fields.Float('Xuất khác', digits=dp.get_precision('Product Unit of Measure'))
    stock_out = fields.Float('Tổng xuất', compute='compute_stock_out', store=True, digits=dp.get_precision('Product Unit of Measure'))

    stock_closing = fields.Float('Tồn cuối kỳ', digits=dp.get_precision('Product Unit of Measure'))
