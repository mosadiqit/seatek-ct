import io, base64, datetime
import logging
from odoo import models

_logger = logging.getLogger(__name__)


class SalesDetailsReportXLS(models.AbstractModel):
    _name = 'report.sea_sales_details_report.sales_details_of_the_date'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):
        worksheet1 = workbook.add_worksheet('Sales Details')
        company_name = self.env.user.company_id.display_name
        company_address = self.env.user.company_id.street + ', ' + self.env.user.company_id.street2 + ', ' + self.env.user.company_id.city
        company_phone = self.env.user.company_id.phone
        company_email = self.env.user.company_id.catchall
        company_logo = io.BytesIO(base64.b64decode(self.env.user.company_id.logo))
        website = self.env.user.company_id.website

        f1 = workbook.add_format(
            {'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
             'font_name': 'Tahoma'})
        f2 = workbook.add_format(
            {'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 10, 'font_name': 'Tahoma'})
        f3 = workbook.add_format({'top': 6, })
        f4 = workbook.add_format(
            {'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 10, 'font_name': 'Tahoma'})
        f5 = workbook.add_format(
            {'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 16,
             'font_name': 'Tahoma'})
        f6 = workbook.add_format(
            {'bold': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 10,
             'font_name': 'Tahoma'})
        f7 = workbook.add_format(
            {'border': 1, 'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 9,
             'font_name': 'Tahoma'})
        f8 = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 9,
             'font_name': 'Tahoma'})
        f9 = workbook.add_format(
            {'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 9,
             'font_name': 'Tahoma'})
        f10 = workbook.add_format(
            {'border': 1, 'bold': 1, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 9,
             'num_format': '#,##0', 'font_name': 'Tahoma'})
        f11 = workbook.add_format(
            {'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 9,
             'num_format': '#,##0', 'font_name': 'Tahoma'})
        f12 = workbook.add_format(
            {'border': 1, 'bold': 1, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 9,
             'num_format': '#,##0', 'font_name': 'Tahoma'})
        f13 = workbook.add_format(
            {'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 10, 'font_name': 'Tahoma'})
        f14 = workbook.add_format(
            {'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 9,
             'font_name': 'Tahoma'})
        f15 = workbook.add_format(
            {'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 8, 'font_name': 'Tahoma'})
        f16 = workbook.add_format(
            {'top': 6, 'bold': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 10,
             'font_name': 'Tahoma'})

        f17 = workbook.add_format(
            {'top': 6, 'bold': 1, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 10,
             'num_format': '#,##0', 'font_name': 'Tahoma'})
        f18 = workbook.add_format(
            {'bold': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 10,
             'font_name': 'Tahoma'})
        f19 = workbook.add_format(
            {'bold': 1, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 10,
             'num_format': '#,##0', 'font_name': 'Tahoma'})

        row_no = 0
        # Report Header
        worksheet1.set_column(0, 0, 1)
        worksheet1.set_column(1, 1, 5)
        worksheet1.set_column(2, 2, 23)
        worksheet1.set_column(3, 3, 6)
        worksheet1.set_column(4, 4, 20)
        worksheet1.set_column(5, 5, 11)
        worksheet1.set_column(6, 6, 11)
        worksheet1.set_column(7, 7, 11)
        worksheet1.set_column(8, 8, 11)

        worksheet1.set_row(0, 22)

        worksheet1.insert_image(0, 2, "company_logo.png",
                                {'image_data': company_logo, 'x_scale': 0.55, 'y_scale': 0.50})

        worksheet1.merge_range(row_no, 4, row_no, 9, company_name, f1)
        row_no += 1
        worksheet1.merge_range(row_no, 4, row_no, 9,
                               'Địa chỉ: ' + company_address, f2)
        row_no += 1
        worksheet1.merge_range(row_no, 4, row_no, 9,
                               'Điện thoại: ' + str(company_phone) + '     Email: ' + company_email, f2)
        row_no += 1
        worksheet1.merge_range(row_no, 1, row_no, 9, ' ', f3)
        row_no += 1
        worksheet1.merge_range(row_no, 1, row_no, 4,
                               'Từ ngày ' + str(objects.start_date.strftime('%d-%m-%Y')) + ' Đến ngày ' + str(
                                   objects.end_date.strftime('%d-%m-%Y')), f4)
        worksheet1.merge_range(row_no, 5, row_no + 1, 9, 'CHI TIẾT HOẠT ĐỘNG TRONG NGÀY', f5)
        row_no += 1
        worksheet1.merge_range(row_no, 1, row_no, 4, 'Thu ngân: ', f4)
        row_no += 1
        worksheet1.merge_range(row_no, 1, row_no, 2, 'BÁN HÀNG', f6)
        row_no += 1
        worksheet1.write(row_no, 1, 'STT', f7)
        worksheet1.write(row_no, 2, 'Số HD', f7)
        worksheet1.write(row_no, 3, 'Giờ tt', f7)
        worksheet1.write(row_no, 4, 'khách hàng', f7)
        worksheet1.write(row_no, 5, 'Tổng cộng', f7)
        worksheet1.write(row_no, 6, 'Tiền mặt', f7)
        worksheet1.write(row_no, 7, 'Chuyển khoản', f7)
        worksheet1.write(row_no, 8, 'Thẻ ATM', f7)
        worksheet1.write(row_no, 9, 'Voucher', f7)
        row_no += 1

        domain = []
        if data.get('start_date'):
            domain.append(('date_order', '>=', data.get('start_date')))
        if data.get('end_date'):
            domain.append(('date_order', '<=', data.get('end_date')))
        if data.get('config_ids'):
            domain.append(('config_id', 'in', data.get('config_ids')))

        # Order Table
        seq = 0
        total = 0
        cash = 0
        bank = 0
        atm = 0
        voucher = 0
        orders = self.env['pos.order'].search(domain)
        for order in reversed(orders):
            seq += 1
            worksheet1.write(row_no, 1, seq, f8)
            worksheet1.write(row_no, 2, order.pos_reference, f8)
            time_tz = datetime.timedelta(hours=7)
            order_real_time = time_tz + order.date_order
            worksheet1.write(row_no, 3, str(order_real_time.strftime('%X'))[:5], f8)
            # worksheet1.write(row_no, 3, str(order.date_order.strftime('%X'))[:5], f8)
            worksheet1.write(row_no, 4, order.partner_id.name, f9)
            worksheet1.write(row_no, 5, order.amount_total, f10)
            total += order.amount_total
            for payment in order.statement_ids:
                if payment.journal_id.id == 127 or payment.journal_id.id == 15 or payment.journal_id.id == 135 \
                        or payment.journal_id.id == 137 or payment.journal_id.id == 138 \
                        or payment.journal_id.id == 139 or payment.journal_id.id == 136:
                    cash += payment.amount
                    worksheet1.write(row_no, 6, payment.amount or 0, f11)
                if payment.journal_id.id == 24:
                    bank += payment.amount
                    worksheet1.write(row_no, 7, payment.amount or 0, f11)
                if payment.journal_id.id == 23:
                    atm += payment.amount
                    worksheet1.write(row_no, 8, payment.amount or 0, f11)
                if payment.journal_id.id == 25:
                    voucher += payment.amount
                    worksheet1.write(row_no, 9, payment.amount or 0, f11)
            row_no += 1
        worksheet1.merge_range(row_no, 1, row_no, 4, 'TỔNG CỘNG', f7)
        worksheet1.write(row_no, 5, total, f12)
        worksheet1.write(row_no, 6, cash, f12)
        worksheet1.write(row_no, 7, bank, f12)
        worksheet1.write(row_no, 8, atm, f12)
        worksheet1.write(row_no, 9, voucher, f12)
        row_no += 2

        worksheet1.merge_range(row_no, 1, row_no, 4, 'Ngày ... Tháng ... Năm 2021', f13)
        worksheet1.merge_range(row_no, 6, row_no, 7, 'TIỀN MẶT', f16)
        worksheet1.merge_range(row_no, 8, row_no, 9, cash, f17)
        row_no += 1
        worksheet1.merge_range(row_no, 1, row_no, 4, 'Người lập', f14)
        worksheet1.merge_range(row_no, 6, row_no, 7, 'CHUYỂN KHOẢN', f18)
        worksheet1.merge_range(row_no, 8, row_no, 9, bank, f19)
        row_no += 1
        worksheet1.merge_range(row_no, 1, row_no, 4, '(Ký, họ tên)', f15)
        worksheet1.merge_range(row_no, 6, row_no, 7, 'TIỀN THẺ', f18)
        worksheet1.merge_range(row_no, 8, row_no, 9, atm, f19)
        row_no += 1
        worksheet1.merge_range(row_no, 6, row_no, 7, 'VOUCHER', f18)
        worksheet1.merge_range(row_no, 8, row_no, 9, voucher, f19)
        row_no += 1
        worksheet1.merge_range(row_no, 6, row_no, 7, 'TRỪ TÍCH LŨY', f18)
        worksheet1.merge_range(row_no, 8, row_no, 9, 0, f19)
        row_no += 1
        worksheet1.merge_range(row_no, 6, row_no, 7, 'KHÁCH HÀNG NỢ', f18)
        worksheet1.merge_range(row_no, 8, row_no, 9, 0, f19)
        row_no += 1
        worksheet1.merge_range(row_no, 6, row_no, 7, 'NỢ NHÀ CUNG CẤP', f18)
        worksheet1.merge_range(row_no, 8, row_no, 9, 0, f19)
        # row_no += 1
        # worksheet1.write(row_no, 4, objects.start_date.strftime('%d-%m-%Y %H:%M:%S'))
        # row_no += 1
        # worksheet1.write(row_no, 4, objects.end_date.strftime('%d-%m-%Y %H:%M:%S'))
