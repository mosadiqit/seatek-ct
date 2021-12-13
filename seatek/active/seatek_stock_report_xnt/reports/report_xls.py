from odoo import models, fields, api, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import datetime
import pytz
import locale
from pytz import timezone
from datetime import timedelta


class Report_Excel(models.AbstractModel):
    _inherit = 'report.report_xlsx.abstract'
    _name = 'report.seatek_stock_report_xnt._report_excel'

    def generate_xlsx_report(self, workbook, data, lines):

        if lines.date_from and lines.date_to:
            date_from_ = lines.date_from.strftime('%d-%m-%Y')
            date_to_ = lines.date_to.strftime('%d-%m-%Y')
        else:
            date_from_ = lines.date_from
            date_to_ = lines.date_to

        worksheet1 = workbook.add_worksheet("Order")

        f1 = workbook.add_format({'bold': True, 'align': 'center', 'font_color': 'black'})
        f2 = workbook.add_format({'align': 'center'})
        f3 = workbook.add_format({'bold': True, 'font_size': 18, 'align': 'center'})
        format_number = workbook.add_format(dict(num_format='#,##0.00'))

        # ---------------------------------------------- #
        row_date_from = 0
        row_date_to = 1
        worksheet1.write(row_date_from, 0, "Từ Ngày")
        worksheet1.write(row_date_to, 0, "Đến Ngày")

        worksheet1.write(row_date_from, 1, date_from_)
        worksheet1.write(row_date_to, 1, date_to_)

        # ---------------------------------------------- #
        worksheet1.write(0, 4, "Địa điểm kho")
        worksheet1.write(1, 4, "Lấy giá trị theo")
        worksheet1.write(2, 4, "Giá trị kho")

        location_col = 5
        for line_location in lines.location_ids:
            worksheet1.write(0, location_col, line_location.name)
            location_col += 1

        worksheet1.write(1, 5, dict(lines._fields['type_get_value'].selection).get(lines.type_get_value))
        worksheet1.write(2, 5, lines.value, format_number)

        # ---------------------------------------------- #
        no1_row = 5
        no1_col = 0

        worksheet1.merge_range('A5:G5', 'CHI TIẾT XUẤT NHẬP TỒN', f3)
        worksheet1.write(no1_row, no1_col, "STT", f1)
        no1_col += 1
        worksheet1.write(no1_row, no1_col, "Tên Sản Phẩm", f1)
        no1_col += 1
        worksheet1.write(no1_row, no1_col, "Đơn Vị", f1)
        no1_col += 1
        worksheet1.write(no1_row, no1_col, "Kho", f1)
        no1_col += 1
        worksheet1.write(no1_row, no1_col, "Đầu Kỳ", f1)
        no1_col += 1
        worksheet1.write(no1_row, no1_col, "Giá trị kho đầu kì", f1)
        no1_col += 1
        worksheet1.write(no1_row, no1_col, "Nhập Trong Kỳ", f1)
        no1_col += 1
        worksheet1.write(no1_row, no1_col, "Giá trị nhập", f1)
        no1_col += 1
        worksheet1.write(no1_row, no1_col, "Xuất Trong Kỳ", f1)
        no1_col += 1
        worksheet1.write(no1_row, no1_col, "Giá trị xuất", f1)
        no1_col += 1
        worksheet1.write(no1_row, no1_col, "Cuối Kỳ", f1)
        no1_col += 1
        worksheet1.write(no1_row, no1_col, "Giá trị kho cuối kì", f1)

        # ---------------------------------------------- #
        sheet_row = 5
        number = 0
        total_stock_opening = 0
        total_stock_in = 0
        total_stock_out = 0
        total_stock_closing = 0

        total_value_opening = 0
        total_value_in = 0
        total_value_out = 0
        total_value_closing = 0

        for line in lines.inventory_report_line_ids_hide_display_product:
            sheet_row += 1
            number += 1
            sheet_col = 0

            worksheet1.write(sheet_row, sheet_col, number, f2)
            sheet_col += 1
            worksheet1.write(sheet_row, sheet_col, line.product_id.name, format_number)
            sheet_col += 1
            worksheet1.write(sheet_row, sheet_col, line.uom_id.name, f2)
            sheet_col += 1
            worksheet1.write(sheet_row, sheet_col, line.location_id.name, f2)
            sheet_col += 1
            worksheet1.write(sheet_row, sheet_col, line.stock_opening, format_number)
            sheet_col += 1
            total_stock_opening += line.stock_opening
            worksheet1.write(sheet_row, sheet_col, line.value_stock_opening, format_number)
            sheet_col += 1
            total_value_opening += line.value_stock_opening
            worksheet1.write(sheet_row, sheet_col, line.stock_in, format_number)
            sheet_col += 1
            total_stock_in += line.stock_in
            worksheet1.write(sheet_row, sheet_col, line.value_stock_in, format_number)
            sheet_col += 1
            total_value_in += line.value_stock_in
            worksheet1.write(sheet_row, sheet_col, line.stock_out, format_number)
            sheet_col += 1
            total_stock_out += line.stock_out
            worksheet1.write(sheet_row, sheet_col, line.value_stock_out, format_number)
            sheet_col += 1
            total_value_out += line.value_stock_out
            worksheet1.write(sheet_row, sheet_col, line.stock_closing, format_number)
            sheet_col += 1
            total_stock_closing += line.stock_closing
            worksheet1.write(sheet_row, sheet_col, line.value_stock_closing, format_number)
            sheet_col += 1
            total_value_closing += line.value_stock_closing


        # custom total
        total_row = sheet_row + 2
        total_col = 3
        merge_range_A_C = 'A' + str(total_row + 1) + ':D' + str(total_row + 1)
        worksheet1.merge_range(merge_range_A_C, '#TỔNG', f3)
        total_col += 1
        worksheet1.write(total_row, total_col, total_stock_opening, format_number)
        total_col += 1
        worksheet1.write(total_row, total_col, total_value_opening, format_number)
        total_col += 1
        worksheet1.write(total_row, total_col, total_stock_in, format_number)
        total_col += 1
        worksheet1.write(total_row, total_col, total_value_in, format_number)
        total_col += 1
        worksheet1.write(total_row, total_col, total_stock_out, format_number)
        total_col += 1
        worksheet1.write(total_row, total_col, total_value_out, format_number)
        total_col += 1
        worksheet1.write(total_row, total_col, total_stock_closing, format_number)
        total_col += 1
        worksheet1.write(total_row, total_col, total_value_closing, format_number)
