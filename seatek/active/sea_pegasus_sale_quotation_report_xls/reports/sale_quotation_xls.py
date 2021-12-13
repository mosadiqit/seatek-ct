import base64
import pytz, io, base64, datetime
from pytz import timezone
from datetime import timedelta
import logging
from odoo import models, api
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)


class SaleQuotationXLS(models.AbstractModel):
    _name = 'report.sea_pegasus_sale_quotation.sale_quotation_xls'
    _inherit = 'report.report_xlsx.abstract'

    def get_address_format(self, company):
        address = ""
        if company.street:
            address += company.street + ", "
        if company.street2:
            address += company.street2 + ", "
        if company.city:
            address += company.city + ", "
        if company.state_id:
            address += company.state_id.name + ", "
        if company.country_id:
            address += company.country_id.name
        return address

    @api.model
    def conver_timezone(self, var):
        user = self.env["res.users"].browse(self._uid)
        tz = timezone(user.tz)
        c_time = datetime.datetime.now(tz)
        hour_tz = int(str(c_time)[-5:][:2])
        min_tz = int(str(c_time)[-5:][3:])
        sign = str(c_time)[-6][:1]
        if sign == '+':
            var_time = datetime.datetime.strptime(str(var), DEFAULT_SERVER_DATETIME_FORMAT or '%Y-%d-%m') + timedelta(
                hours=hour_tz,
                minutes=min_tz)
        else:
            var_time = datetime.datetime.strptime(str(var), DEFAULT_SERVER_DATETIME_FORMAT or '%Y-%d-%m') - timedelta(
                hours=hour_tz,
                minutes=min_tz)
        return str(var_time)

    def generate_xlsx_report(self, workbook, data, objects):
        worksheet1 = workbook.add_worksheet('Sale Quotation')
        company_name = self.env.user.company_id.display_name
        company_logo = io.BytesIO(base64.b64decode(self.env.user.company_id.logo))

        f1 = workbook.add_format(
            {'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 20,
             'font_name': 'Times New Roman', 'font_color': '#00008B'})
        f2 = workbook.add_format(
            {'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 10, 'font_name': 'Times New Roman'})
        f3 = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
             'font_name': 'Times New Roman'})
        f3_1 = workbook.add_format(
            {'bold': 1, 'bottom': 1, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
             'font_name': 'Times New Roman'})
        f4 = workbook.add_format({'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
                                  'font_name': 'Times New Roman'})
        f4_1 = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
                                    'font_name': 'Times New Roman'})
        f5 = workbook.add_format(
            {'bold': 1, 'underline': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
             'font_name': 'Times New Roman'})
        f6 = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
             'font_name': 'Times New Roman'})
        f7 = workbook.add_format(
            {'bold': 1, 'underline': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
             'font_name': 'Times New Roman'})
        f8 = workbook.add_format(
            {'italic': 1, 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12, 'font_name': 'Times New Roman'})
        f9 = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
             'font_name': 'Times New Roman'})
        f10 = workbook.add_format(
            {'border': 1, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
             'font_name': 'Times New Roman'})
        f11 = workbook.add_format(
            {'border': 1, 'valign': 'vcenter', 'text_wrap': True, 'num_format': '#,##0', 'font_size': 12,
             'font_name': 'Times New Roman'})
        f12 = workbook.add_format(
            {'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'num_format': '0.000',
             'font_size': 12, 'font_name': 'Times New Roman'})
        f12_1 = workbook.add_format(
            {'right': 1, 'bottom': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'num_format': '0.000',
             'font_size': 12, 'font_name': 'Times New Roman'})
        f12_2 = workbook.add_format(
            {'bottom': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'num_format': '0.000',
             'font_size': 12, 'font_name': 'Times New Roman'})
        f12_3 = workbook.add_format(
            {'bottom': 1, 'bold': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'num_format': '0.000',
             'font_size': 12, 'font_name': 'Times New Roman'})
        f13 = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bg_color': '#CCFFFF',
             'font_size': 12, 'font_name': 'Times New Roman'})
        f14 = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bg_color': '#CCFFFF',
             'font_size': 12, 'font_name': 'Times New Roman'})
        f15 = workbook.add_format(
            {'valign': 'vcenter', 'text_wrap': True, 'font_size': 12, 'font_name': 'Times New Roman'})
        f16 = workbook.add_format(
            {'italic': 1, 'border': 1, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'num_format': '#,##0',
             'font_size': 12, 'font_name': 'Times New Roman'})
        f17 = workbook.add_format(
            {'align': 'center', 'border': 1, 'valign': 'vcenter', 'text_wrap': True, 'num_format': '#,##0',
             'font_size': 12, 'font_name': 'Times New Roman'})
        f18 = workbook.add_format(
            {'align': 'left', 'border': 1, 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
             'font_name': 'Times New Roman'})
        short_date = workbook.add_format(
            {'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'num_format': 'dd/mmm/yy', 'font_size': 12,
             'font_name': 'Times New Roman'})
        border_short_date = workbook.add_format(
            {'border': 1, 'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'num_format': 'dd/mmm',
             'font_size': 12, 'font_name': 'Times New Roman'})
        money = workbook.add_format(
            {'border': 1, 'bold': 1, 'align': 'right', 'valign': 'vcenter', 'num_format': '#,##0', 'font_size': 12,
             'font_name': 'Times New Roman'})
        money_light = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'num_format': '#,##0', 'font_size': 12,
             'font_name': 'Times New Roman'})
        money_bold_vnd = workbook.add_format(
            {'border': 1, 'bold': 1, 'align': 'right', 'valign': 'vcenter', 'num_format': '#,##0', 'font_size': 12,
             'font_name': 'Times New Roman'})
        money_bold_usd = workbook.add_format(
            {'border': 1, 'bold': 1, 'align': 'right', 'valign': 'vcenter', 'num_format': '#,##0.00', 'font_size': 12,
             'font_name': 'Times New Roman'})
        money_light_vnd = workbook.add_format(
            {'border': 1, 'align': 'right', 'valign': 'vcenter', 'num_format': '#,##0', 'font_size': 12,
             'font_name': 'Times New Roman'})
        money_light_usd = workbook.add_format(
            {'border': 1, 'align': 'right', 'valign': 'vcenter', 'num_format': '#,##0.00', 'font_size': 12,
             'font_name': 'Times New Roman'})

        row_no = 0

        # Report Header
        worksheet1.set_column(0, 0, 11)
        worksheet1.set_column(1, 1, 13)
        worksheet1.set_column(2, 2, 37)
        worksheet1.set_column(3, 3, 8)
        worksheet1.set_column(4, 4, 10)
        worksheet1.set_column(5, 5, 13)
        worksheet1.set_column(6, 6, 13)
        worksheet1.set_column(7, 7, 9)

        worksheet1.insert_image(0, 0, "company_logo.png",
                                {'image_data': company_logo, 'x_scale': 0.25, 'y_scale': 0.2})
        worksheet1.merge_range(row_no, 4, row_no, 7, _('PM-QT-12.03 (04-01/12/2019)'), f2)
        row_no += 1
        worksheet1.merge_range(row_no, 4, row_no, 7, _('SALE QUOTATION'), f1)
        row_no += 1
        worksheet1.write(row_no, 4, _('No:'), f4)
        if objects.partner_id.sea_business_code:
            worksheet1.write(row_no, 5, objects.name + '.' + objects.partner_id.sea_business_code, f4)
        else:
            worksheet1.write(row_no, 5, objects.name, f4)
        worksheet1.merge_range(row_no, 6, row_no, 7, '/' + objects.date_order.strftime('%Y') + '/' + 'BG-PMD', f4_1)
        row_no += 1
        worksheet1.write(row_no, 4, _('Date:'), f4)
        worksheet1.write(row_no, 5, objects.date_order, short_date)
        row_no += 1
        worksheet1.merge_range(row_no, 3, row_no, 4, _('Total of pages: '), f4)
        row_no += 2

        # TO
        worksheet1.write(row_no, 0, _('TO:'), f3)
        worksheet1.merge_range(row_no, 1, row_no, 7, objects.partner_id.display_name, f3)
        row_no += 1
        worksheet1.write(row_no, 0, _('Address:'), f3)
        if objects.sea_temp_delivery_address:
            worksheet1.merge_range(row_no, 1, row_no, 7, objects.sea_temp_delivery_address, f3)
        else:
            worksheet1.merge_range(row_no, 1, row_no, 7, self.get_address_format(objects.partner_id), f3)
        row_no += 1
        worksheet1.write(row_no, 0, _('Tel:'), f3)
        worksheet1.merge_range(row_no, 1, row_no, 3, objects.partner_id.phone or '', f12_2)
        worksheet1.write(row_no, 4, _('Fax: '), f3_1)
        worksheet1.merge_range(row_no, 5, row_no, 7, _(''), f12_1)
        row_no += 1
        worksheet1.write(row_no, 0, _('Email:'), f3)
        worksheet1.merge_range(row_no, 1, row_no, 7, objects.partner_id.email or '', f12)
        row_no += 1
        worksheet1.write(row_no, 0, _('Attn:'), f3)
        if objects.sea_temp_contact:
            worksheet1.merge_range(row_no, 1, row_no, 3, objects.sea_temp_contact, f12_2)
        else:
            for obj in self.env['res.partner'].search([('parent_id', '=', objects.partner_id.id)]):
                if obj.parent_id and obj.type == 'contact':
                    worksheet1.merge_range(row_no, 1, row_no, 3, obj.name, f12_2)
        # for obj in self.env['res.partner'].search([('vat', '=', objects.partner_id.vat)]):
        #     if not obj.custom_type_id.name and obj.parent_id and obj.type == 'contact':
        #         worksheet1.merge_range(row_no, 1, row_no, 3, obj.name, f12)

        worksheet1.write(row_no, 4, _('HP: '), f3_1)
        if not objects.sea_temp_contact:
            for obj in self.env['res.partner'].search([('parent_id', '=', objects.partner_id.id)]):
                if not obj.custom_type_id.name and obj.type == 'contact':
                    worksheet1.merge_range(row_no, 5, row_no, 7, obj.mobile or '', f12_1)
        else:
            worksheet1.merge_range(row_no, 5, row_no, 7, '', f12_1)

        row_no += 2

        # FROM
        worksheet1.write(row_no, 0, _('FROM:'), f3)
        worksheet1.merge_range(row_no, 1, row_no, 7, company_name, f3)
        row_no += 1
        worksheet1.write(row_no, 0, _('Address:'), f3)
        worksheet1.merge_range(row_no, 1, row_no, 7, self.get_address_format(objects.company_id), f3)
        row_no += 1
        worksheet1.write(row_no, 0, _('Tel:'), f3)
        worksheet1.merge_range(row_no, 1, row_no, 3, objects.user_id.company_id.phone or '', f12_2)
        worksheet1.write(row_no, 4, _('Fax: '), f3_1)
        worksheet1.merge_range(row_no, 5, row_no, 7, '', f12_1)
        row_no += 1
        worksheet1.write(row_no, 0, _('Email:'), f3)
        worksheet1.merge_range(row_no, 1, row_no, 7, objects.create_uid.partner_id.email or '', f12)
        row_no += 1
        worksheet1.write(row_no, 0, _('P.I.C:'), f3)
        worksheet1.merge_range(row_no, 1, row_no, 3, objects.create_uid.name or '', f12_3)
        worksheet1.write(row_no, 4, _('HP: '), f3_1)
        worksheet1.merge_range(row_no, 5, row_no, 7, objects.create_uid.partner_id.phone or '', f12_1)
        row_no += 2

        # Reference
        worksheet1.merge_range(row_no, 0, row_no, 2, _("Customer's reference"), f13)
        worksheet1.merge_range(row_no, 3, row_no, 4, _("Pegasus's reference"), f13)
        worksheet1.merge_range(row_no, 5, row_no + 1, 7, _("Currency"), f13)
        row_no += 1
        worksheet1.write(row_no, 0, _('Inquiry No.'), f14)
        worksheet1.write(row_no, 1, _('Inquiry Date'), f14)
        worksheet1.write(row_no, 2, _("Ship's Name"), f14)
        worksheet1.write(row_no, 3, _('Inquiry No.'), f14)
        worksheet1.write(row_no, 4, _('Inquiry Date'), f14)
        row_no += 1
        worksheet1.write(row_no, 0, objects.sea_customer_inquiry_no or '', border_short_date)
        worksheet1.write(row_no, 1, objects.sea_customer_inquiry_date or '', border_short_date)
        if objects.sea_ship_partner_id.name:
            worksheet1.write(row_no, 2, (str(objects.sea_ship_partner_id.name).upper()) or '', border_short_date)
        else:
            worksheet1.write(row_no, 2, objects.partner_id.display_name or '', border_short_date)
        if objects.partner_id.sea_business_code:
            worksheet1.write(row_no, 3, objects.name + '.' + objects.partner_id.sea_business_code, border_short_date)
        else:
            worksheet1.write(row_no, 3, objects.name, border_short_date)
        worksheet1.write(row_no, 4, objects.date_order or '', border_short_date)
        worksheet1.merge_range(row_no, 5, row_no, 7, objects.pricelist_id.currency_id.name, border_short_date)
        row_no += 2

        # Message
        worksheet1.merge_range(row_no, 0, row_no, 7,
                               "Trả lời thư yêu cầu chào hàng trên của Qúy Công ty, chúng tôi xin được báo giá dịch vụ,"
                               "hàng hóa Quý Công ty yêu cầu như sau (Acknowledge to your above inquiry, we hereby "
                               "would like to quote for the services, goods required as follows):", f18)
        row_no += 2

        # Product
        worksheet1.merge_range(row_no, 0, row_no + 1, 0, _("Line's No."), f13)
        worksheet1.merge_range(row_no, 1, row_no, 2, _('Items'), f13)
        unit = ''
        for line in objects.order_line:
            if line.product_id.type == 'service':
                unit += 'Month '
            else:
                unit += 'Unit '
        worksheet1.merge_range(row_no, 3, row_no + 1, 3, unit.split(' ')[0], f13)
        worksheet1.merge_range(row_no, 4, row_no + 1, 4, _("Qty"), f13)
        worksheet1.merge_range(row_no, 5, row_no + 1, 5, _("Unit Price"), f13)
        worksheet1.merge_range(row_no, 6, row_no + 1, 6, _("Line's Value"), f13)
        remark_delivery = ''
        for line in objects.order_line:
            if line.product_id.type == 'service':
                remark_delivery += 'Remark '
            else:
                remark_delivery += 'Delivery '
        worksheet1.merge_range(row_no, 7, row_no + 1, 7, remark_delivery.split(' ')[0], f13)
        row_no += 1
        worksheet1.write(row_no, 1, _('Code'), f13)
        worksheet1.write(row_no, 2, _('Description'), f13)
        row_no += 1

        subtotal_0 = 0
        total_tax_0 = 0
        total_0 = 0
        seq_0 = 1
        total_tax = -1
        for line in objects.order_line:
            if line.tax_id.amount == 0:
                if total_tax == - 1:
                    total_tax = line.tax_id.amount
                worksheet1.write(row_no, 0, seq_0, f17)
                seq_0 += 1
                worksheet1.write(row_no, 1, str(line.product_id.default_code).split('_')[0], f17)
                if line.product_id.type == 'service' and line.product_id.categ_id.name == 'Admiralty Vertor Chart Service' \
                        or line.product_id.type == 'service' and line.product_id.categ_id.name == 'DELIVERY CHARGE':
                    if line.product_id.categ_id.name == 'Admiralty Vertor Chart Service':
                        worksheet1.write(row_no, 2, line.product_id.sea_product_variant_name, f11)
                    else:
                        worksheet1.write(row_no, 2, line.name, f11)
                else:
                    worksheet1.write(row_no, 2, line.product_id.name, f11)
                if line.product_id.type == 'product':
                    if line.product_uom.name:
                        worksheet1.write(row_no, 3, 'Pc', f17)
                else:
                    if line.product_id.categ_id.name == 'DELIVERY CHARGE':
                        worksheet1.write(row_no, 3, 'Pc', f17)
                    else:
                        worksheet1.write(row_no, 3, str(line.product_id.default_code).split('_')[1][:2], f17)
                worksheet1.write(row_no, 4, line.product_uom_qty, f17)
                if objects.pricelist_id.currency_id.name == 'VND':
                    worksheet1.write(row_no, 5, line.price_unit, money_light_vnd)
                    worksheet1.write(row_no, 6, line.price_subtotal, money_light_vnd)
                else:
                    worksheet1.write(row_no, 5, line.price_unit, money_light_usd)
                    worksheet1.write(row_no, 6, line.price_subtotal, money_light_usd)
                worksheet1.write(row_no, 7, line.remarks, f11)
                subtotal_0 += line.price_subtotal
                total_tax_0 += line.price_tax
                total_0 += line.price_total
                row_no += 1
        if total_tax == 0:
            worksheet1.merge_range(row_no, 0, row_no, 4, _('Subtotal Amount:'), f10)
            worksheet1.write(row_no, 5, _(''), f10)
            if objects.pricelist_id.currency_id.name == 'VND':
                worksheet1.write(row_no, 6, subtotal_0, money_light_vnd)
            else:
                worksheet1.write(row_no, 6, subtotal_0, money_light_usd)
            worksheet1.write(row_no, 7, _(''), f10)
            row_no += 1
            worksheet1.merge_range(row_no, 0, row_no, 4, _('Total Tax:'), f16)
            worksheet1.write(row_no, 5, _('0%'), f16)
            if objects.pricelist_id.currency_id.name == 'VND':
                worksheet1.write(row_no, 6, total_tax_0, money_light_vnd)
            else:
                worksheet1.write(row_no, 6, total_tax_0, money_light_usd)
            worksheet1.write(row_no, 7, _(''), f9)
            row_no += 1
            worksheet1.merge_range(row_no, 0, row_no, 4, _('Total Amount:'), f9)
            if objects.amount_untaxed > subtotal_0:
                worksheet1.write(row_no, 5, _('1'), f9)
            else:
                worksheet1.write(row_no, 5, _(''), f9)
            if objects.pricelist_id.currency_id.name == 'VND':
                worksheet1.write(row_no, 6, total_0, money_bold_vnd)
            else:
                worksheet1.write(row_no, 6, total_0, money_bold_usd)
            worksheet1.write(row_no, 7, _(''), f9)
            row_no += 1

        seq_5 = seq_0
        subtotal_5 = 0
        total_tax_5 = 0
        total_5 = 0
        total_tax = -1
        for line in objects.order_line:
            if line.tax_id.amount == 5:
                if total_tax == -1:
                    total_tax = line.tax_id.amount
                worksheet1.write(row_no, 0, seq_5, f17)
                seq_5 += 1
                worksheet1.write(row_no, 1, str(line.product_id.default_code).split('_')[0], f17)
                if line.product_id.type == 'service' and line.product_id.categ_id.name == 'Admiralty Vertor Chart Service' \
                        or line.product_id.type == 'service' and line.product_id.categ_id.name == 'DELIVERY CHARGE':
                    if line.product_id.categ_id.name == 'Admiralty Vertor Chart Service':
                        worksheet1.write(row_no, 2, line.product_id.sea_product_variant_name, f11)
                    else:
                        worksheet1.write(row_no, 2, line.name, f11)
                else:
                    worksheet1.write(row_no, 2, line.product_id.name, f11)
                if line.product_id.type == 'product':
                    if line.product_uom.name:
                        worksheet1.write(row_no, 3, 'Pc', f17)
                else:
                    if line.product_id.categ_id.name == 'DELIVERY CHARGE':
                        worksheet1.write(row_no, 3, 'Pc', f17)
                    else:
                        worksheet1.write(row_no, 3, str(line.product_id.default_code).split('_')[1][:2], f17)
                worksheet1.write(row_no, 4, line.product_uom_qty, f17)
                if objects.pricelist_id.currency_id.name == 'VND':
                    worksheet1.write(row_no, 5, line.price_unit, money_light_vnd)
                    worksheet1.write(row_no, 6, line.price_subtotal, money_light_vnd)
                else:
                    worksheet1.write(row_no, 5, line.price_unit, money_light_usd)
                    worksheet1.write(row_no, 6, line.price_subtotal, money_light_usd)
                worksheet1.write(row_no, 7, line.remarks, f11)
                subtotal_5 += line.price_subtotal
                total_tax_5 += line.price_tax
                total_5 += line.price_total
                row_no += 1
        if total_tax == 5:
            worksheet1.merge_range(row_no, 0, row_no, 4, _('Subtotal Amount:'), f10)
            worksheet1.write(row_no, 5, _(''), f10)
            if objects.pricelist_id.currency_id.name == 'VND':
                worksheet1.write(row_no, 6, subtotal_5, money_light_vnd)
            else:
                worksheet1.write(row_no, 6, subtotal_5, money_light_usd)
            worksheet1.write(row_no, 7, _(''), f10)
            row_no += 1
            worksheet1.merge_range(row_no, 0, row_no, 4, _('Total Tax:'), f16)
            worksheet1.write(row_no, 5, _('5%'), f16)
            if objects.pricelist_id.currency_id.name == 'VND':
                worksheet1.write(row_no, 6, total_tax_5, money_light_vnd)
            else:
                worksheet1.write(row_no, 6, total_tax_5, money_light_usd)
            worksheet1.write(row_no, 7, _(''), f9)
            row_no += 1
            worksheet1.merge_range(row_no, 0, row_no, 4, _('Total Amount:'), f9)
            if objects.amount_untaxed > subtotal_5:
                if subtotal_0 > 0:
                    worksheet1.write(row_no, 5, _('2'), f9)
                else:
                    worksheet1.write(row_no, 5, _('1'), f9)
            else:
                worksheet1.write(row_no, 5, _(''), f9)
            if objects.pricelist_id.currency_id.name == 'VND':
                worksheet1.write(row_no, 6, total_5, money_bold_vnd)
            else:
                worksheet1.write(row_no, 6, total_5, money_bold_usd)
            worksheet1.write(row_no, 7, _(''), f9)
            row_no += 1

        seq_10 = seq_5
        subtotal_10 = 0
        total_tax_10 = 0
        total_10 = 0
        total_tax = -1
        for line in objects.order_line:
            if line.tax_id.amount == 10:
                if total_tax == -1:
                    total_tax = line.tax_id.amount
                worksheet1.write(row_no, 0, seq_10, f17)
                seq_10 += 1
                worksheet1.write(row_no, 1, str(line.product_id.default_code).split('_')[0], f17)
                if line.product_id.type == 'service' and line.product_id.categ_id.name == 'Admiralty Vertor Chart Service' \
                        or line.product_id.type == 'service' and line.product_id.categ_id.name == 'DELIVERY CHARGE':
                    if line.product_id.categ_id.name == 'Admiralty Vertor Chart Service':
                        worksheet1.write(row_no, 2, line.product_id.sea_product_variant_name, f11)
                    else:
                        worksheet1.write(row_no, 2, line.name, f11)
                else:
                    worksheet1.write(row_no, 2, line.product_id.name, f11)
                if line.product_id.type == 'product':
                    if line.product_uom.name:
                        worksheet1.write(row_no, 3, 'Pc', f17)
                else:
                    if line.product_id.categ_id.name == 'DELIVERY CHARGE':
                        worksheet1.write(row_no, 3, 'Pc', f17)
                    else:
                        worksheet1.write(row_no, 3, str(line.product_id.default_code).split('_')[1][:2], f17)
                worksheet1.write(row_no, 4, line.product_uom_qty, f17)
                if objects.pricelist_id.currency_id.name == 'VND':
                    worksheet1.write(row_no, 5, line.price_unit, money_light_vnd)
                    worksheet1.write(row_no, 6, line.price_subtotal, money_light_vnd)
                else:
                    worksheet1.write(row_no, 5, line.price_unit, money_light_usd)
                    worksheet1.write(row_no, 6, line.price_subtotal, money_light_usd)
                worksheet1.write(row_no, 7, line.remarks, f11)
                subtotal_10 += line.price_subtotal
                total_tax_10 += line.price_tax
                total_10 += line.price_total
                row_no += 1
        if total_tax == 10:
            worksheet1.merge_range(row_no, 0, row_no, 4, _('Subtotal Amount:'), f10)
            worksheet1.write(row_no, 5, _(''), f10)
            if objects.pricelist_id.currency_id.name == 'VND':
                worksheet1.write(row_no, 6, subtotal_10, money_light_vnd)
            else:
                worksheet1.write(row_no, 6, subtotal_10, money_light_usd)
            worksheet1.write(row_no, 7, _(''), f10)
            row_no += 1
            worksheet1.merge_range(row_no, 0, row_no, 4, _('Total Tax:'), f16)
            worksheet1.write(row_no, 5, _('10%'), f16)
            if objects.pricelist_id.currency_id.name == 'VND':
                worksheet1.write(row_no, 6, total_tax_10, money_light_vnd)
            else:
                worksheet1.write(row_no, 6, total_tax_10, money_light_usd)
            worksheet1.write(row_no, 7, _(''), f9)
            row_no += 1
            worksheet1.merge_range(row_no, 0, row_no, 4, _('Total Amount:'), f9)
            if objects.amount_untaxed > subtotal_10:
                if subtotal_0 > 0 and subtotal_5 > 0:
                    worksheet1.write(row_no, 5, _('3'), f9)
                elif subtotal_0 > 0 and subtotal_5 == 0:
                    worksheet1.write(row_no, 5, _('2'), f9)
                elif subtotal_0 == 0 and subtotal_5 > 0:
                    worksheet1.write(row_no, 5, _('2'), f9)
            else:
                worksheet1.write(row_no, 5, _(''), f9)
            if objects.pricelist_id.currency_id.name == 'VND':
                worksheet1.write(row_no, 6, total_10, money_bold_vnd)
            else:
                worksheet1.write(row_no, 6, total_10, money_bold_usd)
            worksheet1.write(row_no, 7, _(''), f9)
            row_no += 1

        if subtotal_0 > 0 and subtotal_5 > 0 or subtotal_0 > 0 and subtotal_10 > 0 or subtotal_5 > 0 and subtotal_10 > 0 or subtotal_0 > 0 and subtotal_5 > 0 and subtotal_10 > 0:
            worksheet1.merge_range(row_no, 0, row_no, 4, _('Total Amount:'), f9)
            if subtotal_0 > 0 and subtotal_5 > 0 and subtotal_10 > 0:
                worksheet1.write(row_no, 5, _('1 + 2 + 3'), f9)
            else:
                worksheet1.write(row_no, 5, _('1 + 2'), f9)
            if subtotal_0 > 0 and subtotal_5 > 0 and subtotal_10 == 0:
                if objects.pricelist_id.currency_id.name == 'VND':
                    worksheet1.write(row_no, 6, objects.amount_total, money_bold_vnd)
                else:
                    worksheet1.write(row_no, 6, objects.amount_total, money_bold_usd)
            elif subtotal_0 > 0 and subtotal_10 > 0 and subtotal_5 == 0:
                if objects.pricelist_id.currency_id.name == 'VND':
                    worksheet1.write(row_no, 6, objects.amount_total, money_bold_vnd)
                else:
                    worksheet1.write(row_no, 6, objects.amount_total, money_bold_usd)
            elif subtotal_5 > 0 and subtotal_10 > 0 and subtotal_0 == 0:
                if objects.pricelist_id.currency_id.name == 'VND':
                    worksheet1.write(row_no, 6, objects.amount_total, money_bold_vnd)
                else:
                    worksheet1.write(row_no, 6, objects.amount_total, money_bold_usd)
            elif subtotal_0 > 0 and subtotal_5 > 0 and subtotal_10 > 0:
                if objects.pricelist_id.currency_id.name == 'VND':
                    worksheet1.write(row_no, 6, objects.amount_total, money_bold_vnd)
                else:
                    worksheet1.write(row_no, 6, objects.amount_total, money_bold_usd)
            worksheet1.write(row_no, 7, '', f9)
        row_no += 1

        # Term
        worksheet1.merge_range(row_no, 0, row_no, 7, 'Điều kiện bán hàng (Term of Sale):', f5)
        row_no += 1
        worksheet1.merge_range(row_no, 1, row_no, 7, objects.note, f15)
        # term_of_sale = ''
        # for line in objects.order_line:
        #     if line.product_id.type == 'service':
        #         term_of_sale += 'service '
        #     else:
        #         term_of_sale += 'product '
        # if term_of_sale.split(' ')[0] == 'product':
        #     worksheet1.merge_range(row_no, 1, row_no, 3, _('- Đơn giá không áp dụng VAT (hàng chuyển khẩu)'), f15)
        #     row_no += 1
        #     worksheet1.merge_range(row_no, 1, row_no, 3, _('- Hàng chính hãng mới 100%'), f15)
        #     row_no += 1
        #     worksheet1.merge_range(row_no, 1, row_no, 7,
        #                            _('- Thời gian giao hàng:'), f15)
        #     row_no += 1
        #     worksheet1.merge_range(row_no, 1, row_no, 7,
        #                            _('- Địa điểm giao hàng:'), f15)
        #     row_no += 1
        #     worksheet1.merge_range(row_no, 1, row_no, 7,
        #                            _('- Điều kiện thanh toán:'), f15)
        #     row_no += 1
        #     worksheet1.merge_range(row_no, 1, row_no, 7,
        #                            _('- Hiệu lực báo giá 15 ngày cho toàn bộ đơn hàng'), f15)
        # else:
        #     worksheet1.merge_range(row_no, 1, row_no, 7, '- Hiệu lực báo giá 15 ngày cho toàn bộ đơn hàng.', f15)
        #     row_no += 1
        #     worksheet1.merge_range(row_no, 1, row_no, 7,
        #                            _('- Hàng chính hãng do UKHO sản xuất.'), f15)
        #     row_no += 1
        #     worksheet1.merge_range(row_no, 1, row_no, 7,
        #                            _(
        #                                '- Thời gian giao hành: 1 -2 ngày làm việc đối với công ty đã sử dụng hải đồ điện tử Việt Nam (trừ thứ 7 và Chủ Nhật), 2-4 ngày đối với khách hàng lần đầu sử dụng'),
        #                            f15)
        #     row_no += 1
        #     worksheet1.merge_range(row_no, 1, row_no, 7,
        #                            _(
        #                                '- Thời gian nhận đơn hàng đến 16h cùng ngày, việc hủy hoặc thay đổi đơn hàng cũng chỉ có hiệu lực trong thời gian trên, những đơn hàng sau 16h sẽ được xử lí vào ngày kế tiếp.'),
        #                            f15)
        #     row_no += 1
        #     worksheet1.merge_range(row_no, 1, row_no, 7,
        #                            _(
        #                                '- Giao đĩa update miễn phí trong phạm vi nội ô TPHCM, giao tại các nơi khác phí vận chuyển tính theo cước chuyển phát nhanh'),
        #                            f15)
        #     row_no += 1
        #     worksheet1.merge_range(row_no, 1, row_no, 7,
        #                            _(
        #                                '- Điều kiện thanh toán: thanh toán 100% giá trị đơn hàng trong vòng 30 ngày kể từ ngày nhận đủ chứng từ thanh toán.'),
        #                            f15)
        row_no += 2
        worksheet1.merge_range(row_no, 1, row_no, 3,
                               _('Xác nhận mua hàng (Order Confirmation)'), f7)
        worksheet1.merge_range(row_no, 4, row_no, 7,
                               _('Người chào giá (Quoted by)'), f7)
        row_no += 1
        worksheet1.set_row(row_no, 40, f8)
        worksheet1.merge_range(row_no, 0, row_no, 3,
                               'Nếu Quý Công ty đồng ý mua hàng, vui lòng ký xác nhận vào đây và gửi lại cho chúng tôi để tiến hành cung cấp (If you agreed with our above quotation, please help to sign and stamp here and send back to us for official order)',
                               f8)
