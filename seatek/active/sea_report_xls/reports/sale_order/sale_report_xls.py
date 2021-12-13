# -*- coding: utf-8 -*-
import pytz, io, base64, datetime
from pytz import timezone
from datetime import timedelta
from base64 import b64decode
from logging import getLogger
from PIL import Image
from io import StringIO
from odoo import models, fields, api, exceptions, _
from odoo.fields import Datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class SaleReportXls(models.AbstractModel):
    _inherit = 'report.report_xlsx.abstract'
    _name = 'report.sea_report_xls.sale_order_xls'

    @api.model
    def conver_timezone(self, var):
        if var:
            return Datetime.context_timestamp(self, var).strftime("%d-%m-%Y")
        return ''

    def report_name(self, report_name, name_type):
        if name_type == 'by_effective':
            report_title = report_name + 'NGÀY GIAO HÀNG'
        if name_type == 'by_commitment':
            report_title = report_name + 'NGÀY CAM KẾT'
        if name_type == 'by_order_date':
            report_title = report_name + 'NGÀY ĐẶT HÀNG'
        if name_type == 'by_create_date':
            report_title = report_name + 'NGÀY TẠO ĐƠN HÀNG'
        return report_title

    def warehouse_name(self, objs_wh):
        warehouse = self.env['stock.warehouse'].search([('id', 'in', objs_wh)])
        wh_name = []
        for wh in warehouse:
            wh_name.append(wh.display_name)
        return wh_name

    def generate_xlsx_report(self, workbook, data, wizard):
        self = self.with_context(lang=self.env.user.lang)
        warehouse = self.warehouse_name(data['warehouse'])
        report_name = _('BÁO CÁO CHI TIẾT BÁN HÀNG THEO ')
        worksheet1 = workbook.add_worksheet('BÁO CÁO CHI TIẾT BÁN HÀNG')
        company_name = self.env.user.company_id.display_name
        company_street = self.env.user.company_id.street
        company_street2 = self.env.user.company_id.street2
        company_city = self.env.user.company_id.city
        company_country = self.env.user.company_id.country_id.name
        company_phone = self.env.user.company_id.phone
        company_mail = self.env.user.company_id.catchall
        company_logo = io.BytesIO(base64.b64decode(self.env.user.company_id.logo))
        website = self.env.user.company_id.website

        f1 = workbook.add_format(
            {'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 24})
        f2 = workbook.add_format(
            {'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 10, 'italic': True})
        f3 = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 18})
        f4 = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        f5 = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 9, 'italic': True})
        f6 = workbook.add_format({'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        f7 = workbook.add_format({'bottom': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        f8 = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        f9 = workbook.add_format({'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        f10 = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'italic': True})
        money = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter', 'num_format': '#,##0'})
        percent = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter', 'num_format': 9})
        row_no = 2
        col_no = 0

        # Report header
        worksheet1.set_column(0, 3, 11)
        worksheet1.set_column(4, 5, 30)
        worksheet1.set_column(6, 6, 30)
        worksheet1.set_column(7, 7, 12)
        worksheet1.set_column(8, 9, 10)
        worksheet1.set_column(10, 10, 12)
        worksheet1.set_column(11, 11, 7)
        worksheet1.set_column(12, 15, 12)
        worksheet1.set_column(17, 17, 13)
        # worksheet1.set_column(6, 9, 30)

        worksheet1.freeze_panes(10, 4)
        worksheet1.insert_image(0, 2, "company_logo.png",
                                {'image_data': company_logo, 'x_scale': 0.22, 'y_scale': 0.20})
        worksheet1.merge_range(row_no - 1, 4, row_no, 17, company_name, f1)
        row_no += 1
        worksheet1.merge_range(row_no, 4, row_no, 17,
                               _('Địa chỉ: ') + company_street + _(', ') + str(company_street2) + _(', ') + str(
                                   company_city) + _(', ') + str(company_country), f2)
        row_no += 1
        worksheet1.merge_range(row_no, 4, row_no, 17,
                               _('Điện thoại: ') + str(company_phone) + _('     Email: ') + company_mail, f2)
        row_no += 1
        worksheet1.merge_range(row_no, 4, row_no, 17, website, f2)
        row_no += 1
        worksheet1.merge_range(row_no, 0, row_no, 17, '', f7)
        row_no += 1
        worksheet1.merge_range(row_no, 0, row_no, 3,
                               _('Từ ngày: ') + str(wizard.date_from.strftime('%d-%m-%Y %H:%M:%S')), f5)
        worksheet1.merge_range(row_no, 4, row_no, 17, self.report_name(report_name, wizard.type), f3)
        row_no += 1
        worksheet1.merge_range(row_no, 0, row_no, 3,
                               _('Đến ngày: ') + str(wizard.date_to.strftime('%d-%m-%Y %H:%M:%S')), f5)
        worksheet1.merge_range(row_no, 4, row_no, 17, '(' + ' + '.join(warehouse) + ')' if warehouse else ' ', f5)
        row_no += 1

        # Report worksheet1
        # Header Of Table Data
        worksheet1.write(row_no, col_no, _('Ngày tạo'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Ngày cam kết'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Ngày giao hàng'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Số phiếu'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Khách hàng'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Tên địa chỉ khách hàng'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Mặt hàng bán'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Thực xuất'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Tạm tính'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Ghi chú'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('SL'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Đơn giá'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('%CK'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Tiền giảm'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Thành tiền'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Tiền hàng'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Giảm giá'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Tổng cộng'), f6)

        # End Of Header Table Data
        sheet_row = row_no
        total_all_order_amount_undisc = 0
        total_all_order_amount = 0
        qty_delivery_product_temp = 0
        qty_service_product_temp = 0

        # objs_sale_invoice = self.env['account.invoice'].search([('id', 'in', data['ids'])]).sorted('id')
        # for order_invoice in objs_sale_invoice:
        #     count_line_invoice = list(map(lambda x: x.product_id.id > 0, order_invoice.invoice_line_ids)).count(True)
        #     if count_line_invoice > 1:
        #         for line in order_invoice.invoice_line_ids:
        #             if line.product_id.name == "Phí Vận Chuyển":
        #                 qty_delivery_product_temp = qty_delivery_product_temp + line.quantity
        #             if line.product_id.name == "Phí Dịch Vụ":
        #                 qty_service_product_temp = qty_service_product_temp + line.quantity
        objs_sale = self.env['sale.order'].search([('id', 'in', data['ids'])]).sorted('id')
        for order in objs_sale:
            count_line = list(map(lambda x: x.product_id.id > 0, order.order_line)).count(True)
            if count_line > 1:
                sheet_col = 0
                sheet_row += 1
                line_row = 0
                # Tổng tiền đơn hàng chưa giảm giá
                total_order_amount_undisc = 0
                # Số tiền giảm giá cho đơn hàng, chưa áp dụng
                total_order_disc = 0
                # Số tiền giảm giá cho đơn hàng, chưa áp dụng
                total_order_amount = 0
                # Số tiền phí vận chuyển
                total_price_shipping = 0
                # Số tiền phí dịch vụ
                total_price_service = 0;
                for line in order.order_line:
                    if line.product_id:
                        line_col = sheet_col + 5
                        # Tỷ lệ giảm giá
                        discount = line.discount / 100
                        # Đặt số lượng cho Vận chuyển
                        qty_delivery_product = 0
                        if line.product_id.name == 'Phí Vận Chuyển':
                            if line.qty_invoiced:
                                qty_delivery_product += line.qty_invoiced
                            else:
                                qty_delivery_product += line.product_uom_qty
                        # Đặt số lượng cho Dịch vụ
                        qty_service_product = 0
                        if line.product_id.name == 'Phí Dịch Vụ':
                            if line.qty_invoiced:
                                qty_service_product += line.qty_invoiced
                            else:
                                qty_service_product += line.product_uom_qty
                        # Số tiền giảm giá mỗi sản phẩm
                        price_discount_line = line.qty_invoiced * line.price_unit * discount
                        # Tổng tiền hàng sản khi đã giảm giá
                        total_price_line = (line.qty_invoiced * line.price_unit) - price_discount_line
                        # Tổng tiền phí vận chuyển
                        if line.product_id.name == 'Phí Vận Chuyển':
                            total_price_shipping += (qty_delivery_product * line.price_unit) - price_discount_line
                        # Tổng tiền phí dịch vụ
                        elif line.product_id.name == 'Phí Dịch Vụ':
                            total_price_service += (qty_service_product * line.price_unit) - price_discount_line
                        else:
                            # Tổng tiền hàng sản khi đã giảm giá
                            total_price_line = (line.qty_invoiced * line.price_unit) - price_discount_line

                        # Tính tổng giảm giá đơn hàng
                        if line.product_id.name == 'Phí Vận Chuyển':
                            if line.qty_invoiced:
                                total_order_amount_undisc += total_price_line
                            else:
                                total_order_amount_undisc += (total_price_line + total_price_shipping)
                        elif line.product_id.name == 'Phí Dịch Vụ':
                            if line.qty_invoiced:
                                total_order_amount_undisc += total_price_line
                            else:
                                total_order_amount_undisc += (total_price_line + total_price_service)
                        else:
                            total_order_amount_undisc += (
                                        total_price_line - (total_price_shipping + total_price_service))
                        # Tiền tạm tính mỗi line
                        amount_draft = line.qty_delivered * line.price_unit * (1 - discount)
                        worksheet1.write(sheet_row + line_row, line_col, line.product_id.name, f4)
                        line_col += 1
                        worksheet1.write(sheet_row + line_row, line_col, line.product_id.name, f4)
                        line_col += 1

                        if line.product_id.name == 'Phí Vận Chuyển':
                            worksheet1.write(sheet_row + line_row, line_col, qty_delivery_product, f4)
                        elif line.product_id.name == 'Phí Dịch Vụ':
                            worksheet1.write(sheet_row + line_row, line_col, qty_service_product, f4)
                        else:
                            worksheet1.write(sheet_row + line_row, line_col, line.qty_delivered, f4)
                        line_col += 1
                        worksheet1.write(sheet_row + line_row, line_col, amount_draft, money)
                        line_col += 1
                        worksheet1.write(sheet_row + line_row, line_col, line.remarks, f4)
                        line_col += 1
                        if line.product_id.name == 'Phí Vận Chuyển':
                            worksheet1.write(sheet_row + line_row, line_col, qty_delivery_product, f4)
                        elif line.product_id.name == 'Phí Dịch Vụ':
                            worksheet1.write(sheet_row + line_row, line_col, qty_service_product, f4)
                        else:
                            worksheet1.write(sheet_row + line_row, line_col, line.qty_invoiced, f4)
                        line_col += 1
                        worksheet1.write(sheet_row + line_row, line_col, line.price_unit, money)
                        line_col += 1
                        worksheet1.write(sheet_row + line_row, line_col, discount, percent)
                        line_col += 1
                        worksheet1.write(sheet_row + line_row, line_col, price_discount_line, money)
                        line_col += 1
                        if line.product_id.name == 'Phí Vận Chuyển':
                            worksheet1.write(sheet_row + line_row, line_col, total_price_shipping, money)
                        elif line.product_id.name == 'Phí Dịch Vụ':
                            worksheet1.write(sheet_row + line_row, line_col, total_price_service, money)
                        else:
                            worksheet1.write(sheet_row + line_row, line_col, total_price_line, money)
                        line_row += 1

                # Tổng giá trị đơn hàng sau khi đã giảm giá
                total_order_amount = total_order_amount_undisc - total_order_disc
                line_count = line_row - 1
                worksheet1.merge_range(sheet_row, sheet_col, sheet_row + line_count, sheet_col,
                                       self.conver_timezone(order.create_date), f4)
                sheet_col += 1
                worksheet1.merge_range(sheet_row, sheet_col, sheet_row + line_count, sheet_col,
                                       self.conver_timezone(order.commitment_date), f4)
                sheet_col += 1

                effective_date = ''
                if order.effective_date:
                    effective_date = order.effective_date.strftime('%d-%m-%Y')

                worksheet1.merge_range(sheet_row, sheet_col, sheet_row + line_count, sheet_col, effective_date, f4)
                sheet_col += 1
                worksheet1.merge_range(sheet_row, sheet_col, sheet_row + line_count, sheet_col, order.name, f4)
                sheet_col += 1
                worksheet1.merge_range(sheet_row, sheet_col, sheet_row + line_count, sheet_col, order.partner_id.name,
                                       f4)
                sheet_col += 1
                worksheet1.merge_range(sheet_row, sheet_col, sheet_row + line_count, sheet_col,
                                       order.partner_shipping_id.name, f4)
                sheet_col += 10
                # Tổng tiền hàng chưa giảm giá
                worksheet1.merge_range(sheet_row, sheet_col, sheet_row + line_count, sheet_col,
                                       total_order_amount_undisc, money)

                sheet_col += 1
                worksheet1.merge_range(sheet_row, sheet_col, sheet_row + line_count, sheet_col, '0', money)
                sheet_col += 1
                # Tổng tiền hàng đã giảm

                worksheet1.merge_range(sheet_row, sheet_col, sheet_row + line_count, sheet_col,
                                       total_order_amount,
                                       money)

                total_all_order_amount_undisc = total_order_amount_undisc + total_all_order_amount_undisc
                total_all_order_amount = total_order_amount_undisc + total_all_order_amount - total_order_disc
                sheet_row += line_count
            else:
                # Tổng tiền đơn hàng chưa giảm giá
                total_order_amount_undisc = 0
                # Số tiền giảm giá cho đơn hàng, chưa áp dụng
                total_order_disc = 0
                # Số tiền giảm giá cho đơn hàng, chưa áp dụng
                total_order_amount = 0
                for line in order.order_line:
                    if line.product_id:
                        sheet_col = 0
                        sheet_row += 1
                        # Tỷ lệ giảm giá
                        discount = line.discount / 100
                        # Số tiền giảm giá mỗi sản phẩm
                        price_discount_line = line.qty_invoiced * line.price_unit * discount
                        # Tổng tiền hàng sản khi đã giảm giá
                        total_price_line = (line.qty_invoiced * line.price_unit) - price_discount_line
                        # Tính tổng giảm giá đơn hàng
                        total_order_amount_undisc += total_price_line
                        # Tổng giá trị đơn hàng sau khi đã giảm giá
                        total_order_amount = total_order_amount_undisc - total_order_disc
                        # Tiền tạm tính mỗi line
                        amount_draft = line.qty_delivered * line.price_unit * (1 - discount)

                        worksheet1.write(sheet_row, sheet_col, self.conver_timezone(order.create_date), f4)
                        sheet_col += 1
                        worksheet1.write(sheet_row, sheet_col, self.conver_timezone(order.commitment_date), f4)
                        sheet_col += 1
                        effective_date = ''
                        if order.effective_date:
                            effective_date = order.effective_date.strftime('%d-%m-%Y')
                        worksheet1.write(sheet_row, sheet_col, effective_date, f4)
                        sheet_col += 1
                        worksheet1.write(sheet_row, sheet_col, order.name, f4)
                        sheet_col += 1
                        worksheet1.write(sheet_row, sheet_col, order.partner_id.name, f4)
                        sheet_col += 1
                        worksheet1.write(sheet_row, sheet_col, order.partner_shipping_id.name, f4)
                        sheet_col += 1
                        worksheet1.write(sheet_row, sheet_col, line.product_id.name, f4)
                        sheet_col += 1
                        worksheet1.write(sheet_row, sheet_col, line.qty_delivered, f4)
                        sheet_col += 1
                        worksheet1.write(sheet_row, sheet_col, amount_draft, money)
                        sheet_col += 1
                        worksheet1.write(sheet_row, sheet_col, line.remarks, f4)
                        sheet_col += 1
                        worksheet1.write(sheet_row, sheet_col, line.qty_invoiced, f4)
                        sheet_col += 1
                        worksheet1.write(sheet_row, sheet_col, line.price_unit, money)
                        sheet_col += 1
                        worksheet1.write(sheet_row, sheet_col, discount, percent)
                        sheet_col += 1
                        worksheet1.write(sheet_row, sheet_col, price_discount_line, money)
                        sheet_col += 1
                        worksheet1.write(sheet_row, sheet_col, total_price_line, money)
                        sheet_col += 1
                        percent_tax = (line.price_unit * line.tax_id.amount) / 100
                        worksheet1.write(sheet_row, sheet_col, total_order_amount_undisc, money)
                        sheet_col += 1
                        worksheet1.write(sheet_row, sheet_col, '0', money)
                        sheet_col += 1
                        worksheet1.write(sheet_row, sheet_col, total_order_amount, money)
                        total_all_order_amount_undisc += total_order_amount_undisc
                        total_all_order_amount += total_order_amount_undisc - total_order_disc
        worksheet1.merge_range(sheet_row + 1, 0, sheet_row + 1, 14, _('TỔNG CỘNG'), f3)
        worksheet1.write(sheet_row + 1, 15, total_all_order_amount_undisc, money)
        worksheet1.write(sheet_row + 1, 16, '0', money)
        worksheet1.write(sheet_row + 1, 17, total_all_order_amount, money)
        worksheet1.merge_range(sheet_row + 3, 10, sheet_row + 3, 15, _('____, ____/____/20___'), f8)
        worksheet1.merge_range(sheet_row + 4, 10, sheet_row + 4, 15, _('Người lập'), f9)
        worksheet1.merge_range(sheet_row + 5, 10, sheet_row + 5, 15, _('(Ký, ghi rõ họ tên)'), f10)
