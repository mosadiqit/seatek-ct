import io, base64, datetime
import logging
from odoo import models

_logger = logging.getLogger(__name__)


class SalesDetailsReportXLS(models.AbstractModel):
    _name = 'report.sea_sales_details_report.sales_details_by_date'
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
            {'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 10, 'font_name': 'Tahoma'})
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
            {'border': 1, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 9,
             'num_format': '#,##0', 'font_name': 'Tahoma'})
        f11 = workbook.add_format(
            {'border': 1, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 9,
             'num_format': '#,##0.00', 'font_name': 'Tahoma'})

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

        row_no = 0
        # Report Header
        worksheet1.set_column(0, 0, 1)
        worksheet1.set_column(1, 1, 10)
        worksheet1.set_column(2, 2, 23)
        worksheet1.set_column(3, 3, 15)
        worksheet1.set_column(4, 4, 25)
        worksheet1.set_column(5, 5, 6)
        worksheet1.set_column(6, 6, 10)
        worksheet1.set_column(7, 7, 6)
        worksheet1.set_column(8, 8, 10)
        worksheet1.set_column(9, 9, 12)
        worksheet1.set_column(10, 10, 10)
        worksheet1.set_column(11, 11, 10)
        worksheet1.set_column(12, 12, 12)
        worksheet1.set_column(13, 13, 13)

        worksheet1.set_row(3, 7)
        worksheet1.set_row(4, 12)
        worksheet1.set_row(7, 7)
        worksheet1.set_row(0, 22)

        worksheet1.insert_image(0, 2, "company_logo.png",
                                {'image_data': company_logo, 'x_scale': 0.60, 'y_scale': 0.55})

        worksheet1.merge_range(row_no, 3, row_no, 13, company_name, f1)
        row_no += 1
        worksheet1.merge_range(row_no, 3, row_no, 13,
                               'Địa chỉ: ' + company_address, f2)
        row_no += 1
        worksheet1.merge_range(row_no, 3, row_no, 13,
                               'Điện thoại: ' + str(company_phone) + '     Email: ' + company_email, f2)
        row_no += 1
        worksheet1.merge_range(row_no, 1, row_no, 13, ' ')
        row_no += 1
        worksheet1.merge_range(row_no, 1, row_no, 13, ' ', f3)
        row_no += 1
        worksheet1.merge_range(row_no, 1, row_no, 13, 'BÁO CÁO CHI TIẾT BÁN HÀNG THEO NGÀY', f5)
        row_no += 1
        worksheet1.merge_range(row_no, 1, row_no, 13,
                               'Từ ngày ' + str(objects.start_date.strftime('%d-%m-%Y')) + ' Đến ngày ' + str(
                                   objects.end_date.strftime('%d-%m-%Y')), f4)
        row_no += 1
        worksheet1.merge_range(row_no, 1, row_no, 13, ' ')
        row_no += 1
        worksheet1.write(row_no, 1, 'Ngày', f7)
        worksheet1.write(row_no, 2, 'Số phiếu', f7)
        worksheet1.write(row_no, 3, 'Khách hàng', f7)
        worksheet1.write(row_no, 4, 'Mặt hàng bán', f7)
        worksheet1.write(row_no, 5, 'SL', f7)
        worksheet1.write(row_no, 6, 'Đơn giá', f7)
        worksheet1.write(row_no, 7, '%CK', f7)
        worksheet1.write(row_no, 8, 'Tiền giảm', f7)
        worksheet1.write(row_no, 9, 'Thành tiền', f7)
        worksheet1.write(row_no, 10, 'Tiền hàng', f7)
        worksheet1.write(row_no, 11, 'Giảm giá', f7)
        worksheet1.write(row_no, 12, 'Tổng cộng', f7)
        worksheet1.write(row_no, 13, 'Thanh toán', f7)
        row_no += 1

        domain = []
        if data.get('start_date'):
            domain.append(('date_order', '>=', data.get('start_date')))
        if data.get('end_date'):
            domain.append(('date_order', '<=', data.get('end_date')))
        if data.get('config_ids'):
            domain.append(('config_id', 'in', data.get('config_ids')))

        # Order Table
        subtotal = 0
        discount = 0
        total = 0
        paid = 0
        orders = self.env['pos.order'].search(domain)
        for order in reversed(orders):
            count_order_line = list(map(lambda x: x.product_id.id > 0, order.lines)).count(True)
            if count_order_line > 1:
                time_tz = datetime.timedelta(hours=7)
                order_real_time = time_tz + order.date_order
                worksheet1.merge_range(row_no, 1, row_no + count_order_line - 1, 1,
                                       str(order_real_time.strftime('%d/%m/%Y')), f8)
                worksheet1.merge_range(row_no, 2, row_no + count_order_line - 1, 2, order.pos_reference, f8)
                worksheet1.merge_range(row_no, 3, row_no + count_order_line - 1, 3, order.partner_id.name, f9)
            else:
                time_tz = datetime.timedelta(hours=7)
                order_real_time = time_tz + order.date_order
                worksheet1.write(row_no, 1, str(order_real_time.strftime('%d/%m/%Y')), f8)
                worksheet1.write(row_no, 2, order.pos_reference, f8)
                worksheet1.write(row_no, 3, order.partner_id.name, f9)
            for line in order.lines:
                worksheet1.write(row_no, 4, line.product_id.name, f9)
                worksheet1.write(row_no, 5, line.qty, f11)
                worksheet1.write(row_no, 6, line.price_unit, f10)
                worksheet1.write(row_no, 7, line.discount, f10)
                worksheet1.write(row_no, 8, 0, f10)
                worksheet1.write(row_no, 9, line.price_subtotal_incl, f10)
                row_no += 1
            if count_order_line > 1:
                worksheet1.merge_range(row_no - count_order_line, 10, row_no - 1, 10, order.amount_total, f10)
                subtotal += order.amount_total
                worksheet1.merge_range(row_no - count_order_line, 11, row_no - 1, 11, 0, f10)
                worksheet1.merge_range(row_no - count_order_line, 12, row_no - 1, 12, order.amount_total, f10)
                total += order.amount_total
                worksheet1.merge_range(row_no - count_order_line, 13, row_no - 1, 13, order.amount_paid, f10)
                paid += order.amount_paid
            else:
                worksheet1.write(row_no - 1, 10, order.amount_total, f10)
                subtotal += order.amount_total
                worksheet1.write(row_no - 1, 11, 0, f10)

                worksheet1.write(row_no - 1, 12, order.amount_total, f10)
                total += order.amount_total
                worksheet1.write(row_no - 1, 13, order.amount_paid, f10)
                paid += order.amount_paid
        worksheet1.merge_range(row_no, 1, row_no, 9, 'TỔNG CỘNG', f7)
        worksheet1.write(row_no, 10, subtotal, f12)
        worksheet1.write(row_no, 11, discount, f12)
        worksheet1.write(row_no, 12, total, f12)
        worksheet1.write(row_no, 13, paid, f12)
        row_no += 1

        worksheet1.merge_range(row_no, 9, row_no, 13, 'Ngày ... Tháng ... Năm 2021', f13)
        row_no += 1
        worksheet1.merge_range(row_no, 9, row_no, 13, 'Người lập', f14)
        row_no += 1
        worksheet1.merge_range(row_no, 9, row_no, 13, '(Ký, họ tên)', f15)

