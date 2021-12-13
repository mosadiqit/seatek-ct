import pytz, io, base64, datetime
from pytz import timezone
from datetime import timedelta
import logging
from odoo import models, api
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)


class ProFormaReportXLS(models.AbstractModel):
    _name = 'report.sea_pegasus_proforma_invoice_xls.proforma_invoice_xls'
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
            address += company.state_id.name + ', '
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
        worksheet1 = workbook.add_worksheet('PRO-FORMA Invoice')
        company_logo = io.BytesIO(base64.b64decode(self.env.user.company_id.logo))

        f1 = workbook.add_format({'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 10,
                                  'font_name': 'Times New Roman'})
        f2 = workbook.add_format(
            {'bold': 1, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 18,
             'font_name': 'Times New Roman', 'font_color': '#00008B'})

        f3 = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
             'font_name': 'Times New Roman'})
        f3_1 = workbook.add_format(
            {'bold': 1, 'border': 1, 'underline': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 12, 'font_name': 'Times New Roman'})
        f3_2 = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 12, 'font_name': 'Times New Roman'})
        f4 = workbook.add_format({'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
                                  'font_name': 'Times New Roman'})
        f5 = workbook.add_format({'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
                                  'font_name': 'Times New Roman'})
        f6 = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True})
        f7 = workbook.add_format(
            {'bold': 1, 'underline': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        f8 = workbook.add_format({'italic': 1, 'valign': 'vcenter', 'text_wrap': True})
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
            {'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'num_format': '0.000'})
        f13 = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bg_color': '#CCFFFF',
             'font_size': 12,
             'font_name': 'Times New Roman'})
        f14 = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bg_color': '#ADD8E6'})
        f15 = workbook.add_format({'valign': 'vcenter', 'text_wrap': True})
        f16 = workbook.add_format(
            {'italic': 1, 'border': 1, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'num_format': '#,##0',
             'font_size': 12,
             'font_name': 'Times New Roman'})
        f17 = workbook.add_format(
            {'align': 'center', 'border': 1, 'valign': 'vcenter', 'text_wrap': True, 'num_format': '#,##0',
             'font_size': 12,
             'font_name': 'Times New Roman'})
        f18 = workbook.add_format(
            {'bold': 1, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
             'font_name': 'Times New Roman'})
        short_date = workbook.add_format(
            {'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'num_format': 'dd/mmm/yy',
             'font_size': 12,
             'font_name': 'Times New Roman'})
        border_short_date = workbook.add_format(
            {'border': 1, 'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'num_format': 'dd/mmm',
             'font_size': 12,
             'font_name': 'Times New Roman'})
        border_short_date_alt = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'num_format': 'dd/mmm',
             'font_size': 12,
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

        # Format column
        worksheet1.set_column(0, 0, 11.7)
        worksheet1.set_column(1, 1, 15)
        worksheet1.set_column(2, 2, 30.7)
        worksheet1.set_column(3, 3, 11.7)
        worksheet1.set_column(4, 4, 9.7)
        worksheet1.set_column(5, 5, 15.3)
        worksheet1.set_column(6, 6, 16.1)

        worksheet1.insert_image(0, 0, "company_logo.png",
                                {'image_data': company_logo, 'x_scale': 0.22, 'y_scale': 0.2})
        worksheet1.merge_range(row_no, 4, row_no, 6, _('PM-QT-12.03 (04-01/12/2019)'), f1)
        row_no += 1
        worksheet1.merge_range(row_no, 3, row_no, 6, _('PRO FORMA INVOICE'), f2)
        row_no += 1
        worksheet1.merge_range(row_no, 3, row_no, 6, _('Also considered as Sale Confirmation'), f18)
        row_no += 1
        worksheet1.write(row_no, 4, _('PI No: '), f4)
        if objects.partner_id.sea_business_code:
            worksheet1.write(row_no, 5, str(objects.name) + '.' + str(objects.partner_id.sea_business_code), f4)
            worksheet1.write(row_no, 6, str('/' + objects.date_order.strftime("%Y") + '/PI-PMD'), f5)
        else:
            worksheet1.write(row_no, 5, str(objects.name), f4)
            worksheet1.write(row_no, 6, str('/' + objects.date_order.strftime("%Y") + '/PI-PMD'), f5)
        row_no += 1
        worksheet1.write(row_no, 4, _('PI Date: '), f4)
        pi_date = ''
        for line in objects.order_line:
            if line.product_id.type == 'product':
                pi_date += 'product '
        if pi_date.split(' ')[0] == 'product':
            date_done = ''
            for obj in self.env['stock.picking'].search([('origin', '=', objects.name)]):
                if obj.date_done:
                    date_done = date_done + obj.date_done.strftime("%d/%b/%y")
            if date_done:
                worksheet1.write(row_no, 5, date_done[0:9], short_date)
        else:
            if objects.confirmation_date:
                worksheet1.write(row_no, 5, objects.confirmation_date, short_date)
        row_no += 1
        worksheet1.write(row_no, 6, _('pages'), f5)
        row_no += 2

        # Invoice To
        invoice_delivery = ''
        for line in objects.order_line:
            if line.product_id.type == 'product':
                invoice_delivery += 'product '
        invoice_delivery_temp = invoice_delivery.split(' ')[0]
        if invoice_delivery_temp == 'product':
            worksheet1.write(row_no, 0, _('Invoice To:'), f3_1)
            # worksheet1.merge_range(row_no, 1, row_no, 2, objects.partner_invoice_id.name, f3)
            if objects.partner_id.is_company == True:
                worksheet1.merge_range(row_no, 1, row_no, 2, objects.partner_id.name, f3)
            else:
                worksheet1.merge_range(row_no, 1, row_no, 2, objects.partner_id.parent_id.name, f3)
            worksheet1.write(row_no, 3, _('Deliver To:'), f3_2)
            # worksheet1.merge_range(row_no, 4, row_no, 6, objects.partner_shipping_id.name, f3)
            if objects.partner_id.is_company == True:
                worksheet1.merge_range(row_no, 4, row_no, 6, objects.partner_id.name, f3)
            else:
                worksheet1.merge_range(row_no, 4, row_no, 6, objects.partner_id.parent_id.name, f3)
            row_no += 1
            worksheet1.write(row_no, 0, _('Add:'), f3)
            worksheet1.merge_range(row_no, 1, row_no, 2, self.get_address_format(objects.partner_invoice_id), f11)
            worksheet1.write(row_no, 3, _('Add:'), f3)
            if objects.sea_temp_delivery_address:
                worksheet1.merge_range(row_no, 4, row_no, 6, objects.sea_temp_delivery_address, f11)
            else:
                worksheet1.merge_range(row_no, 4, row_no, 6, self.get_address_format(objects.partner_shipping_id), f11)
            row_no += 1
            worksheet1.write(row_no, 0, _('Tax Code:'), f3)
            if objects.partner_id.vat:
                worksheet1.merge_range(row_no, 1, row_no, 2, objects.partner_id.vat, f11)
            else:
                worksheet1.merge_range(row_no, 1, row_no, 2, '', f11)
            worksheet1.write(row_no, 3, _('Attn:'), f3)
            if objects.sea_temp_contact:
                worksheet1.merge_range(row_no, 4, row_no, 6, objects.sea_temp_contact, f3)
            else:
                for obj in self.env['res.partner'].search([('parent_id', '=', objects.partner_id.id)]):
                    if not obj.custom_type_id.name and obj.parent_id and obj.type == 'contact':
                        if obj.name and obj.mobile:
                            worksheet1.merge_range(row_no, 4, row_no, 6, str(obj.name) + ' / ' + str(obj.mobile), f3)
                        else:
                            worksheet1.merge_range(row_no, 4, row_no, 6, obj.name, f3)
            row_no += 2
        else:
            worksheet1.write(row_no, 0, _('Invoice To:'), f3_1)
            # worksheet1.merge_range(row_no, 1, row_no, 2, objects.partner_invoice_id.name, f3)
            if objects.partner_id.is_company == True:
                worksheet1.merge_range(row_no, 1, row_no, 2, objects.partner_id.name, f3)
            else:
                worksheet1.merge_range(row_no, 1, row_no, 2, objects.partner_id.parent_id.name, f3)
            worksheet1.write(row_no, 3, _('Deliver To:'), f3_2)
            if objects.sea_ship_partner_id.name:
                worksheet1.merge_range(row_no, 4, row_no, 6, (str(objects.sea_ship_partner_id.name).upper()) or '', f3)
            else:
                if objects.partner_id.is_company == True:
                    worksheet1.merge_range(row_no, 4, row_no, 6, objects.partner_id.name, f3)
                else:
                    worksheet1.merge_range(row_no, 4, row_no, 6, objects.partner_id.parent_id.name, f3)
                # worksheet1.merge_range(row_no, 4, row_no, 6, objects.partner_shipping_id.name, f3)
            row_no += 1
            worksheet1.write(row_no, 0, _('Add.:'), f3)
            worksheet1.merge_range(row_no, 1, row_no, 2, self.get_address_format(objects.partner_id), f11)
            worksheet1.write(row_no, 3, _(' '), f3)
            worksheet1.merge_range(row_no, 4, row_no, 6, _(' '), f11)
            row_no += 1
            worksheet1.write(row_no, 0, _('Tax Code:'), f3)
            worksheet1.merge_range(row_no, 1, row_no, 2, objects.partner_id.vat or '', f11)
            worksheet1.merge_range(row_no, 3, row_no, 6, _(' '), f3)

            row_no += 2

            # Reference
        worksheet1.merge_range(row_no, 0, row_no, 2, _("Customer's reference"), f13)
        worksheet1.merge_range(row_no, 3, row_no + 1, 3, _("Pegasus's reference"), f13)
        worksheet1.merge_range(row_no, 4, row_no + 1, 4, _("Dispatch Date"), f13)
        worksheet1.merge_range(row_no, 5, row_no + 1, 5, _("Payment Due Date"), f13)
        worksheet1.merge_range(row_no, 6, row_no + 1, 6, _("Currency"), f13)
        row_no += 1
        worksheet1.write(row_no, 0, _("Order No."), f13)
        worksheet1.write(row_no, 1, _("Order Date"), f13)
        worksheet1.write(row_no, 2, _("Ship's name"), f13)
        row_no += 1
        worksheet1.write(row_no, 0, objects.sea_customer_po_no or '', border_short_date_alt)
        worksheet1.write(row_no, 1, objects.confirmation_date or '', border_short_date_alt)
        if objects.sea_ship_partner_id.name:
            worksheet1.write(row_no, 2, (str(objects.sea_ship_partner_id.name).upper()) or '', border_short_date)
        else:
            if objects.partner_id.is_company == True:
                worksheet1.write(row_no, 2, objects.partner_id.name, border_short_date)
            else:
                worksheet1.write(row_no, 2, objects.partner_id.parent_id.name, border_short_date)
        # worksheet1.write(row_no, 3, objects.sea_customer_inquiry_no or '', border_short_date)
        if objects.partner_id.sea_business_code:
            worksheet1.write(row_no, 3, str(objects.name) + '.' + str(objects.partner_id.sea_business_code),
                             border_short_date)
        else:
            worksheet1.write(row_no, 3, str(objects.name), border_short_date)

        dispatch_date = ''
        for line in objects.order_line:
            if line.product_id.type == 'product':
                dispatch_date += 'product '
        if dispatch_date.split(' ')[0] == 'product':
            date_done = ''
            for obj in self.env['stock.picking'].search([('origin', '=', objects.name)]):
                if obj.date_done:
                    date_done = date_done + obj.date_done.strftime("%d/%b")
            worksheet1.write(row_no, 4, date_done[0:6], border_short_date)
        else:
            worksheet1.write(row_no, 4, objects.confirmation_date or '', border_short_date)

        # worksheet1.write(row_no, 4, objects.date_order or '', border_short_date)

        worksheet1.write(row_no, 5, _(''), border_short_date)
        worksheet1.write(row_no, 6, objects.currency_id.name, border_short_date_alt)
        row_no += 2

        # Product
        worksheet1.merge_range(row_no, 0, row_no + 1, 0, _("Line's No."), f13)
        worksheet1.merge_range(row_no, 1, row_no + 1, 1, _("Code"), f13)
        worksheet1.merge_range(row_no, 2, row_no + 1, 2, _("Description"), f13)
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
        row_no += 2

        subtotal_0 = 0
        total_tax_0 = 0
        total_0 = 0
        seq_0 = 1
        total_tax = -1
        qty_delivered = 0
        amount_untaxed = 0
        product_service = ''
        for line in objects.order_line:
            qty_delivered = line.qty_delivered
            amount_untaxed += line.sea_price_total_qty_delivered
            if line.product_id.type == 'product':
                product_service = 'product ' + product_service
            else:
                product_service = 'service ' + product_service
            if line.tax_id.amount == 0:
                if total_tax == -1:
                    total_tax = line.tax_id.amount
                if line.product_id.type == 'service' or line.qty_delivered:
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
                    if line.product_id.type == 'service':
                        worksheet1.write(row_no, 4, line.product_uom_qty, f17)
                    else:
                        worksheet1.write(row_no, 4, line.qty_delivered, f17)
                    if objects.pricelist_id.currency_id.name == 'VND':
                        worksheet1.write(row_no, 5, line.price_unit, money_light_vnd)
                        if line.product_id.type == 'service':
                            worksheet1.write(row_no, 6, line.price_subtotal, money_light_vnd)
                            subtotal_0 += line.price_subtotal
                            total_0 += line.price_total
                        else:
                            worksheet1.write(row_no, 6, line.sea_price_total_qty_delivered, money_light_vnd)
                            subtotal_0 += line.sea_price_total_qty_delivered
                            total_0 += line.sea_price_total_qty_delivered
                    else:
                        worksheet1.write(row_no, 5, line.price_unit, money_light_usd)
                        if line.product_id.type == 'service':
                            worksheet1.write(row_no, 6, line.price_subtotal, money_light_usd)
                            subtotal_0 += line.price_subtotal
                            total_0 += line.price_total
                        else:
                            worksheet1.write(row_no, 6, line.sea_price_total_qty_delivered, money_light_usd)
                            subtotal_0 += line.sea_price_total_qty_delivered
                            total_0 += line.sea_price_total_qty_delivered
                    total_tax_0 += line.price_tax
                    row_no += 1
        if qty_delivered or product_service.split(' ')[0] == 'service':
            if total_tax == 0:
                worksheet1.merge_range(row_no, 0, row_no, 4, _('Subtotal Amount:'), f10)
                worksheet1.write(row_no, 5, _(''), f10)
                if objects.pricelist_id.currency_id.name == 'VND':
                    worksheet1.write(row_no, 6, subtotal_0, money_light_vnd)
                else:
                    worksheet1.write(row_no, 6, subtotal_0, money_light_usd)
                row_no += 1
                worksheet1.merge_range(row_no, 0, row_no, 4, _('Total Tax:'), f16)
                worksheet1.write(row_no, 5, _('0%'), f16)
                if objects.pricelist_id.currency_id.name == 'VND':
                    worksheet1.write(row_no, 6, total_tax_0, money_light_vnd)
                else:
                    worksheet1.write(row_no, 6, total_tax_0, money_light_usd)
                row_no += 1
                worksheet1.merge_range(row_no, 0, row_no, 4, _('Total Amount:'), f9)
                if amount_untaxed > subtotal_0:
                    worksheet1.write(row_no, 5, _('1'), f9)
                else:
                    worksheet1.write(row_no, 5, _(''), f9)

                if objects.pricelist_id.currency_id.name == 'VND':
                    worksheet1.write(row_no, 6, total_0, money_bold_vnd)
                else:
                    worksheet1.write(row_no, 6, total_0, money_bold_usd)
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
                if line.product_id.type == 'service' or line.qty_delivered:
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
                    if line.product_id.type == 'service':
                        worksheet1.write(row_no, 4, line.product_uom_qty, f17)
                    else:
                        worksheet1.write(row_no, 4, line.qty_delivered, f17)
                    if objects.pricelist_id.currency_id.name == 'VND':
                        worksheet1.write(row_no, 5, line.price_unit, money_light_vnd)
                        if line.product_id.type == 'service':
                            worksheet1.write(row_no, 6, line.price_subtotal, money_light_vnd)
                            subtotal_5 += line.price_subtotal
                            total_5 += line.price_total
                        else:
                            worksheet1.write(row_no, 6, line.sea_price_total_qty_delivered, money_light_vnd)
                            subtotal_5 += line.sea_price_total_qty_delivered
                            total_5 = line.sea_price_total_qty_delivered + line.sea_price_total_qty_delivered * 0.05
                    else:
                        worksheet1.write(row_no, 5, line.price_unit, money_light_usd)
                        if line.product_id.type == 'service':
                            worksheet1.write(row_no, 6, line.price_subtotal, money_light_usd)
                            subtotal_5 += line.price_subtotal
                            total_5 += line.price_total
                        else:
                            worksheet1.write(row_no, 6, line.sea_price_total_qty_delivered, money_light_usd)
                            subtotal_5 += line.sea_price_total_qty_delivered
                            total_5 = line.sea_price_total_qty_delivered + line.sea_price_total_qty_delivered * 0.05
                    row_no += 1
        if qty_delivered or product_service.split(' ')[0] == 'service':
            if total_tax == 5:
                worksheet1.merge_range(row_no, 0, row_no, 4, _('Subtotal Amount:'), f10)
                worksheet1.write(row_no, 5, _(''), f10)
                if objects.pricelist_id.currency_id.name == 'VND':
                    worksheet1.write(row_no, 6, subtotal_5, money_light_vnd)
                else:
                    worksheet1.write(row_no, 6, subtotal_5, money_light_usd)
                row_no += 1
                worksheet1.merge_range(row_no, 0, row_no, 4, _('Total Tax:'), f16)
                worksheet1.write(row_no, 5, _('5%'), f16)
                if objects.pricelist_id.currency_id.name == 'VND':
                    worksheet1.write(row_no, 6, subtotal_5 * 0.05, money_light_vnd)
                else:
                    worksheet1.write(row_no, 6, subtotal_5 * 0.05, money_light_usd)
                row_no += 1
                worksheet1.merge_range(row_no, 0, row_no, 4, _('Total Amount:'), f9)
                if amount_untaxed > subtotal_5:
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
                if line.product_id.type == 'service' or line.qty_delivered:
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
                    if line.product_id.type == 'service':
                        worksheet1.write(row_no, 4, line.product_uom_qty, f17)
                    else:
                        worksheet1.write(row_no, 4, line.qty_delivered, f17)
                    if objects.pricelist_id.currency_id.name == 'VND':
                        worksheet1.write(row_no, 5, line.price_unit, money_light_vnd)
                        if line.product_id.type == 'service':
                            worksheet1.write(row_no, 6, line.price_subtotal, money_light_vnd)
                            subtotal_10 += line.price_subtotal
                            total_10 += line.price_total
                        else:
                            worksheet1.write(row_no, 6, line.sea_price_total_qty_delivered, money_light_vnd)
                            subtotal_10 += line.sea_price_total_qty_delivered
                            total_10 = line.sea_price_total_qty_delivered + line.sea_price_total_qty_delivered * 0.1
                    else:
                        worksheet1.write(row_no, 5, line.price_unit, money_light_usd)
                        if line.product_id.type == 'service':
                            worksheet1.write(row_no, 6, line.price_subtotal, money_light_usd)
                            subtotal_10 += line.price_subtotal
                            total_10 += line.price_total
                        else:
                            worksheet1.write(row_no, 6, line.sea_price_total_qty_delivered, money_light_usd)
                            subtotal_10 += line.sea_price_total_qty_delivered
                            total_10 = line.sea_price_total_qty_delivered + line.sea_price_total_qty_delivered * 0.1
                    row_no += 1
        if qty_delivered or product_service.split(' ')[0] == 'service':
            if total_tax == 10:
                worksheet1.merge_range(row_no, 0, row_no, 4, _('Subtotal Amount:'), f10)
                worksheet1.write(row_no, 5, _(''), f10)
                if objects.pricelist_id.currency_id.name == 'VND':
                    worksheet1.write(row_no, 6, subtotal_10, money_light_vnd)
                else:
                    worksheet1.write(row_no, 6, subtotal_10, money_light_usd)
                row_no += 1
                worksheet1.merge_range(row_no, 0, row_no, 4, _('Total Tax:'), f16)
                worksheet1.write(row_no, 5, _('10%'), f16)
                if objects.pricelist_id.currency_id.name == 'VND':
                    worksheet1.write(row_no, 6, subtotal_10 * 0.1, money_light_vnd)
                else:
                    worksheet1.write(row_no, 6, subtotal_10 * 0.1, money_light_usd)
                row_no += 1
                worksheet1.merge_range(row_no, 0, row_no, 4, _('Total Amount:'), f9)
                if amount_untaxed > subtotal_10:
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
                row_no += 1

        if subtotal_0 > 0 and subtotal_5 > 0 or subtotal_0 > 0 and subtotal_10 > 0 or subtotal_5 > 0 and subtotal_10 > 0 or subtotal_0 > 0 and subtotal_5 > 0 and subtotal_10 > 0:
            worksheet1.merge_range(row_no, 0, row_no, 4, _('Total Amount:'), f9)
            if subtotal_0 > 0 and subtotal_5 > 0 and subtotal_10 > 0:
                worksheet1.write(row_no, 5, _('1 + 2 + 3'), f9)
            else:
                worksheet1.write(row_no, 5, _('1 + 2'), f9)
            if subtotal_0 > 0 and subtotal_5 > 0 and subtotal_10 == 0:
                if objects.pricelist_id.currency_id.name == 'VND':
                    worksheet1.write(row_no, 6, total_0 + total_5, money_bold_vnd)
                else:
                    worksheet1.write(row_no, 6, total_0 + total_5, money_bold_usd)
            elif subtotal_0 > 0 and subtotal_10 > 0 and subtotal_5 == 0:
                if objects.pricelist_id.currency_id.name == 'VND':
                    worksheet1.write(row_no, 6, total_0 + total_10, money_bold_vnd)
                else:
                    worksheet1.write(row_no, 6, total_0 + total_10, money_bold_usd)
            elif subtotal_5 > 0 and subtotal_10 > 0 and subtotal_0 == 0:
                if objects.pricelist_id.currency_id.name == 'VND':
                    worksheet1.write(row_no, 6, total_5 + total_10, money_bold_vnd)
                else:
                    worksheet1.write(row_no, 6, total_5 + total_10, money_bold_usd)
            elif subtotal_0 > 0 and subtotal_5 > 0 and subtotal_10 > 0:
                if objects.pricelist_id.currency_id.name == 'VND':
                    worksheet1.write(row_no, 6, total_0 + total_5 + total_10, money_bold_vnd)
                else:
                    worksheet1.write(row_no, 6, total_0 + total_5 + total_10, money_bold_usd)
        row_no += 2
        worksheet1.merge_range(row_no, 0, row_no, 6, _("Payment's Details:"), workbook.add_format(
            {'bold': 1, 'border': 1, 'bottom': 0, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_name': 'Times New Roman'}))
        row_no += 1
        worksheet1.merge_range(row_no, 0, row_no, 6, _(''), workbook.add_format(
            {'border': 1, 'top': 0, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, }))
        row_no += 2
        worksheet1.merge_range(row_no, 0, row_no + 1, 6, _(
            "*** Additional Infomation: Nếu có nhu cầu xuất hóa đơn, xin quý khách vui lòng liên hệ trong vòng 7 ngày kể từ ngày giao hàng."),
                               workbook.add_format(
                                   {'bold': 1, 'border': 1, 'valign': 'vcenter', 'text_wrap': True,
                                    'font_name': 'Times New Roman'}))
        row_no += 3
        worksheet1.insert_textbox(row_no, 0, ' ',
                                  {'border': {'color': 'black'}, 'x_offset': 15, 'width': 250, 'height': 140})
        worksheet1.insert_textbox(row_no, 2, ' ',
                                  {'border': {'color': 'black'}, 'x_offset': 80, 'width': 250, 'height': 140})
        worksheet1.insert_textbox(row_no, 4, ' ',
                                  {'border': {'color': 'black'}, 'x_offset': 35, 'width': 250, 'height': 140})
