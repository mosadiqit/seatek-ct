# -*- coding: utf-8 -*-
import pytz, io, base64, datetime
from dateutil.relativedelta import relativedelta
from pytz import timezone
from datetime import timedelta
from base64 import b64decode
from logging import getLogger
from PIL import Image
from io import StringIO
from odoo import models, fields, api, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class EmployeeListXls(models.AbstractModel):
    _inherit = 'report.report_xlsx.abstract'
    _name = 'report.sea_employee_extend.employee_list_report_xls'

    @api.model
    def conver_timezone(self, var):
        user = self.env["res.users"].browse(self._uid)
        tz = timezone(user.tz)
        c_time = datetime.datetime.now(tz)
        hour_tz = int(str(c_time)[-5:][:2])
        min_tz = int(str(c_time)[-5:][3:])
        sign = str(c_time)[-6][:1]
        if sign == '+':
            var_time = datetime.datetime.strptime(str(var), '%Y-%m-%d') + timedelta(hours=hour_tz,
                                                                                                        minutes=min_tz)
        else:
            var_time = datetime.datetime.strptime(str(var), '%Y-%m-%d') - timedelta(hours=hour_tz,
                                                                                                        minutes=min_tz)
        return var_time.strftime("%d-%m-%Y")

    @api.model
    def calculate_year_month_day(self, var):
        now = datetime.datetime.now()
        time_difference = relativedelta(now, var)
        years = time_difference.years
        months = time_difference.months
        days = time_difference.days
        return years, months, days

    @api.model

    def generate_xlsx_report(self, workbook, data, wizard):
        list_employee = self.env['hr.employee'].search([('id', 'in', data['ids'])]).sorted('id')
        report_name = _('DỮ LIỆU NHÂN SỰ')
        # report_ctx = self.report_ctx(data['product'], data['location'], data['picking_type'])
        worksheet1 = workbook.add_worksheet(_('DỮ LIỆU NHÂN SỰ'))
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
        f11 = workbook.add_format({'border': 1, 'valign': 'vcenter', 'text_wrap': True})
        f12 = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'num_format': '0.000'})
        money = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter', 'num_format': '#,##0'})
        percent = workbook.add_format({'border': 1, 'num_format': 9, 'align': 'center', 'valign': 'vcenter', })
        row_no = 0
        col_no = 0

        # Report header
        worksheet1.set_column(0, 0, 5)
        worksheet1.set_column(1, 2, 13)
        worksheet1.set_column(3, 3, 18)
        worksheet1.set_column(4, 5, 22)
        worksheet1.set_column(6, 6, 8)
        worksheet1.set_column(7, 7, 30)
        worksheet1.set_column(8, 8, 8)
        worksheet1.set_column(9, 9, 12)
        worksheet1.set_column(10, 10, 7)
        worksheet1.set_column(11, 11, 12)
        worksheet1.set_column(12, 12, 15)
        worksheet1.set_column(14, 14, 12)
        worksheet1.set_column(16, 16, 12)
        worksheet1.freeze_panes(10, 2)
        worksheet1.autofilter(9, 0, 9, 14)
        worksheet1.insert_image(row_no, 1, "company_logo.png",
                                {'image_data': company_logo, 'x_scale': 0.19, 'y_scale': 0.17})
        worksheet1.merge_range(row_no, 2, row_no + 1, 14, company_name, f1)
        row_no += 2
        worksheet1.merge_range(row_no, 2, row_no, 16,
                               _('Địa chỉ: ') + company_street + _(', ') + str(company_street2) + _(', ') + str(
                                   company_city) + _(', ') + str(company_country), f2)
        row_no += 1
        worksheet1.merge_range(row_no, 2, row_no, 16,
                               _('Điện thoại: ') + str(company_phone) + _('     Email: ') + company_mail, f2)
        row_no += 1
        worksheet1.merge_range(row_no, 2, row_no, 16, website, f2)
        row_no += 3

        # Report worksheet1
        # Header Of Table Data
        worksheet1.write(row_no, col_no, _('STT'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Mã nhân viên'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Họ tên'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Giới tính'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Ngày vào hệ thống SEACORP'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Ngày ký HĐLĐ chính thức'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Năm'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Tháng'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Ngày'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Ngày vào ĐVTV'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Phòng ban'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Chức vụ'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Công việc đảm nhận'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Ngày tháng năm sinh'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Tháng sinh nhật'), f6)
        col_no += 1
        # cmnd
        worksheet1.write(row_no, col_no, _('Số '), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Ngày cấp'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Nơi cấp'), f6)
        col_no += 1
        # hộ chiếu
        worksheet1.write(row_no, col_no, _('Số '), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Ngày cấp'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Nơi cấp'), f6)
        col_no += 1

        worksheet1.write(row_no, col_no, _('Quê quán'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Địa chỉ thường trú'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Địa chỉ tạm trú'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Trình độ học vấn'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Trình độ chuyên môn'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Dân tộc'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Tôn giáo'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Tình trạng hôn nhân'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Điện thoại'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Email công ty'), f6)
        col_no += 1

        # info người thân
        worksheet1.write(row_no, col_no, _('Họ tên'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Điện thoại'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Địa chỉ'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Quan hệ'), f6)
        col_no += 1

        # info con cái
        worksheet1.write(row_no, col_no, _('Số con'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Họ tên con'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Năm sinh'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Giới tính'), f6)
        col_no += 1

        # info thuế tncn
        worksheet1.write(row_no, col_no, _('Mã số thuế TNCN'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Số người phụ thuộc'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Tên người phụ thuộc, mã số người phụ thuộc'), f6)
        col_no += 1

        # info bhxh
        worksheet1.write(row_no, col_no, _('Số sổ BHXH'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Thực trạng'), f6)
        col_no += 1

        worksheet1.write(row_no, col_no, _('Số TK ngân hàng'), f6)
        col_no += 1

        # info contract
        worksheet1.write(row_no, col_no, _('Hình thức hợp đồng'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Thời hạn hợp đồng'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Số hợp đồng'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Ngày ký hợp đồng'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Ngày hết hạn hợp đồng'), f6)
        col_no += 1

        # info work status
        worksheet1.write(row_no, col_no, _('Làm việc/Nghỉ chế độ/ Thôi việc'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Lý do'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Ngày nghỉ'), f6)
        col_no += 1

        # contract 1
        worksheet1.write(row_no, col_no, _('Hợp đồng 1'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Ngày ký'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Ngày hết hạn'), f6)
        col_no += 1

        # contract 2
        worksheet1.write(row_no, col_no, _('Hợp đồng 2'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Ngày ký'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Ngày hết hạn'), f6)
        col_no += 1

        # contract 3
        worksheet1.write(row_no, col_no, _('Hợp đồng 3'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Ngày ký'), f6)
        col_no += 1
        worksheet1.write(row_no, col_no, _('Ngày hết hạn'), f6)
        col_no += 1

        worksheet1.write(row_no, col_no, _('Ghi chú'), f6)
        col_no += 1

        # End Of Header Table Data
        sheet_row = row_no
        quantity = 0
        value = 0
        seq = 0
        quantity_remarks = 0
        quantity_price = 0
        for employee in list_employee:
            contract = self.env['hr.contract'].search([('employee_id', '=', employee.id),
            ('active', '=', 't'), ('state', 'in', ['draft','open','pending'])],
            order='create_date desc',
            limit=1)
            years, months, days = self.calculate_year_month_day(employee.seagroup_join_date)
            sheet_col = 0
            sheet_row += 1
            seq += 1
            # worksheet1.write(sheet_row, sheet_col, seq, f4)
            # sheet_col += 1
            # worksheet1.write(sheet_row, sheet_col, self.conver_timezone(line.date)[0:10], f4)
            # sheet_col += 1
            # if line.picking_id.date_done:
            #     worksheet1.write(sheet_row, sheet_col, self.conver_timezone(line.picking_id.date_done)[0:10], f4)
            # else:
            #     worksheet1.write(sheet_row, sheet_col, '*', f4)
            # sheet_col += 1
            # worksheet1.write(sheet_row, sheet_col,
            #                     line.picking_id.display_name if line.picking_id.display_name else _('Hao hụt'), f4)
            # sheet_col += 1
                    # worksheet1.write(sheet_row, sheet_col, employee.user_id, f4)
                    # sheet_col += 1
            worksheet1.write(sheet_row, sheet_col, seq, f4)
            sheet_col += 1
            worksheet1.write(sheet_row, sheet_col, employee.employee_code, f4)
            sheet_col += 1
            worksheet1.write(sheet_row, sheet_col, employee.name, f11)
            sheet_col += 1
            worksheet1.write(sheet_row, sheet_col, employee.gender, f4)
            sheet_col += 1
            worksheet1.write(sheet_row, sheet_col, employee.seagroup_join_date.strftime("%d-%m-%Y") if employee.seagroup_join_date != False else "", f12)
            sheet_col += 1
            worksheet1.write(sheet_row, sheet_col, employee.official_contract.strftime("%d-%m-%Y") if employee.official_contract != False else "", f12)
            sheet_col += 1
            worksheet1.write(sheet_row, sheet_col, years, f4)
            sheet_col += 1
            worksheet1.write(sheet_row, sheet_col, months, f4)
            sheet_col += 1
            worksheet1.write(sheet_row, sheet_col, days, f4)
            sheet_col += 1
            worksheet1.write(sheet_row, sheet_col, contract.create_date.strftime("%d-%m-%Y") if contract.create_date != False else "", f4)
            sheet_col += 1
            worksheet1.write(sheet_row, sheet_col, employee.department_id.name if employee.department_id.name != False else "", f4)
            sheet_col += 1
            worksheet1.write(sheet_row, sheet_col, employee.job_title if employee.job_title != False else "", f4)
            sheet_col += 1
            worksheet1.write(sheet_row, sheet_col, employee.job_id.name if employee.job_id.name != False else "", f4)
            sheet_col += 1
            worksheet1.write(sheet_row, sheet_col, employee.birthday.strftime("%d-%m-%Y") if employee.birthday != False else "", f4)
            sheet_col += 1
            worksheet1.write(sheet_row, sheet_col, employee.birthday.month if employee.birthday != False else "", f4)
            sheet_col += 1

            worksheet1.write(sheet_row, sheet_col, employee.identification_id, f4)
            sheet_col += 1
            worksheet1.write(sheet_row, sheet_col, employee.identification_issue_date.strftime("%d-%m-%Y") if employee.identification_issue_date != False else "", f4)
            sheet_col += 1
            worksheet1.write(sheet_row, sheet_col, employee.identification_issue_office, f4)
            sheet_col += 1

            worksheet1.write(sheet_row, sheet_col, employee.passport_id, f4)
            sheet_col += 1
            worksheet1.write(sheet_row, sheet_col, employee.passport_issue_date.strftime("%d-%m-%Y") if employee.passport_issue_date != False else "", f4)
            sheet_col += 1
            worksheet1.write(sheet_row, sheet_col, employee.passport_issue_office, f4)
            sheet_col += 1

            worksheet1.write(sheet_row, sheet_col, employee.home_town, f4)
            sheet_col += 1
            worksheet1.write(sheet_row, sheet_col, employee.address_home_id.name, f4)
            sheet_col += 1
            worksheet1.write(sheet_row, sheet_col, employee.temporary_address.name, f4)
            sheet_col += 1
            # if line.lot_id.name != False:
            #     worksheet1.write(sheet_row, sheet_col, line.lot_id.name, f12)
            # else:
            #     worksheet1.write(sheet_row, sheet_col, '', f12)

            # sheet_col += 1
            # worksheet1.write(sheet_row, sheet_col, line.product_id.lst_price, money)
            # sheet_col += 1
            # worksheet1.write(sheet_row, sheet_col, line.qty_done * line.product_id.lst_price or '0', money)
            # quantity += line.qty_done
            # value += (line.qty_done * line.product_id.standard_price)
        # sheet_row += 1
        # worksheet1.merge_range(sheet_row, 0, sheet_row, 8, _('TỔNG CỘNG'), f3)
        # worksheet1.write(sheet_row, 9, quantity, f4)
        # worksheet1.write(sheet_row, 10, '', f4)
        # worksheet1.write(sheet_row, 11, '', money)
        # worksheet1.write(sheet_row, 12, abs(value), money)
        # worksheet1.write(sheet_row, 13, '', f4)
        # worksheet1.write(sheet_row, 14, '', f4)
        # worksheet1.write(sheet_row, 15, '', f4)
        # worksheet1.write(sheet_row, 16, '', f4)
        # worksheet1.merge_range(sheet_row + 2, 0, sheet_row + 2, 4, _('____, ____/____/20___'), f8)
        # worksheet1.merge_range(sheet_row + 2, 6, sheet_row + 2, 15, _('____, ____/____/20___'), f8)
        # worksheet1.merge_range(sheet_row + 3, 0, sheet_row + 3, 4, _('Trưởng phòng'), f9)
        # worksheet1.merge_range(sheet_row + 3, 6, sheet_row + 3, 15, 'Người lập', f9)
        # worksheet1.merge_range(sheet_row + 4, 0, sheet_row + 4, 4, '(Ký, họ tên)', f10)
        # worksheet1.merge_range(sheet_row + 4, 6, sheet_row + 4, 15, '(Ký, họ tên)', f10)
