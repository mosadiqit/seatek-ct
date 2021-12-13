# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import datetime
import pytz
from pytz import timezone
from datetime import timedelta


class PosSessionXls(models.AbstractModel):
    _inherit = 'report.report_xlsx.abstract'
    _name = 'report.sea_report_xls.pos_session_xls'

    @api.model
    def conver_timezone(self, var):
        user = self.env["res.users"].browse(self._uid)
        tz = timezone(user.tz)
        c_time = datetime.datetime.now(tz)
        hour_tz = int(str(c_time)[-5:][:2])
        min_tz = int(str(c_time)[-5:][3:])
        sign = str(c_time)[-6][:1]
        if sign == '+':
            var_time = datetime.datetime.strptime(str(var)[0:19], DEFAULT_SERVER_DATETIME_FORMAT) + timedelta(hours=hour_tz, minutes=min_tz)
        else:
            var_time = datetime.datetime.strptime(str(var)[0:19], DEFAULT_SERVER_DATETIME_FORMAT) - timedelta(hours=hour_tz, minutes=min_tz)
        return str(var_time)

    def report_session(self, session_id):
        search_order = [('session_id', '=', session_id.id)]
        objs_order = self.env['pos.order'].search(search_order)
        return objs_order
        
    def report_time(self):
        pass
    def report_user(self):
        pass

    def generate_xlsx_report(self, workbook, data, wizard):

        if wizard.type == 'time':
            self.report_time()
        elif wizard.type == 'user':
            self.report_user()
        else:
            objs_order = self.report_session(wizard.session_id)

        worksheet1 = workbook.add_worksheet("POS Order")
        no1_row = 0
        no1_col = 0
        worksheet2 = workbook.add_worksheet("Order Detail")
        no2_row = 0
        no2_col = 0

        f1 = workbook.add_format({'bold': True, 'font_color': 'black', })
        f2 = workbook.add_format({'font_size': 20, 'align': 'left','bold': True})
        blue = workbook.add_format({'bold': True, 'font_color': 'blue', })
        gray = workbook.add_format({'bold': True, 'font_color': 'gray', })
        red = workbook.add_format({'bold': True, 'font_color': 'red', })
        green = workbook.add_format({'bold': True, 'font_color': 'green', })
        money = workbook.add_format({'num_format': '#,##0 $'})

# Report worksheet1
    # Header Of Table Data
        worksheet1.write(no1_row, no1_col, "Create Date", f1)
        no1_col += 1
        worksheet1.write(no1_row, no1_col, "Order Name", f1)
        no1_col += 1
        worksheet1.write(no1_row, no1_col, "Partner Name", f1)
        no1_col += 1
        worksheet1.write(no1_row, no1_col, "Amount", f1)
        no1_col += 1
        worksheet1.write(no1_row, no1_col, "Tax", f1)
        no1_col += 1
        worksheet1.write(no1_row, no1_col, "Total", f1)
        no1_col += 1
        worksheet1.write(no1_row, no1_col, "Order State", f1)

    # End Of Header Table Data
        sheet_row1 = 0
        for sheet1 in objs_order:
            sheet_col1 = 0
            sheet_row1 += 1
            worksheet1.freeze_panes(1, 2)
            worksheet1.write(sheet_row1, sheet_col1, self.conver_timezone(sheet1.create_date)[0:16])
            sheet_col1 += 1
            worksheet1.write(sheet_row1, sheet_col1, sheet1.name or ' ')
            sheet_col1 += 1
            worksheet1.write(sheet_row1, sheet_col1, sheet1.partner_id.display_name or ' ')
            sheet_col1 += 1
            worksheet1.write(sheet_row1, sheet_col1, sheet1.amount_paid, money)
            sheet_col1 += 1
            worksheet1.write(sheet_row1, sheet_col1, abs(sheet1.amount_tax), money)
            sheet_col1 += 1
            worksheet1.write(sheet_row1, sheet_col1, abs(sheet1.amount_total), money)
            sheet_col1 += 1
            worksheet1.write(sheet_row1, sheet_col1, sheet1.state or ' ')

# Report worksheet2
    # Header Of Table Data
        worksheet2.write(no2_row, no2_col, "Order Name", f1)
        no2_col += 1
        worksheet2.write(no2_row, no2_col, "Barcode", f1)
        no2_col += 1
        worksheet2.write(no2_row, no2_col, "Internal Reference", f1)
        no2_col += 1
        worksheet2.write(no2_row, no2_col, "Product Name", f1)
        no2_col += 1
        worksheet2.write(no2_row, no2_col, "Category", f1)
        no2_col += 1
        worksheet2.write(no2_row, no2_col, "Price", f1)
        no2_col += 1
        worksheet2.write(no2_row, no2_col, "Quantity", f1)
        no2_col += 1
        worksheet2.write(no2_row, no2_col, "Tax", f1)
        no2_col += 1
        worksheet2.write(no2_row, no2_col, "Total", f1)

    # End Of Header Table Data
        sheet_row2 = 0
        for objs_line in objs_order:
            for sheet2 in objs_line.lines:
                sheet_row2 += 1
                sheet_col2 = 0
                worksheet2.freeze_panes(1, 1)
                worksheet2.write(sheet_row2, sheet_col2, sheet2.order_id.name if sheet2.order_id.name else ' ')
                sheet_col2 += 1
                worksheet2.write(sheet_row2, sheet_col2, sheet2.product_id.barcode or ' ')
                sheet_col2 += 1
                worksheet2.write(sheet_row2, sheet_col2, sheet2.product_id.code or ' ')
                sheet_col2 += 1
                worksheet2.write(sheet_row2, sheet_col2, sheet2.product_id.name)
                sheet_col2 += 1
                worksheet2.write(sheet_row2, sheet_col2, sheet2.product_id.categ_id.display_name or ' ')
                sheet_col2 += 1
                worksheet2.write(sheet_row2, sheet_col2, sheet2.price_unit or ' ', money)
                sheet_col2 += 1
                worksheet2.write(sheet_row2, sheet_col2, abs(sheet2.qty) or ' ')
                sheet_col2 += 1
                worksheet2.write(sheet_row2, sheet_col2, sheet2.tax_ids.name or ' ', money)
                sheet_col2 += 1
                worksheet2.write(sheet_row2, sheet_col2, abs(sheet2.price_subtotal) or ' ', money)
            break
