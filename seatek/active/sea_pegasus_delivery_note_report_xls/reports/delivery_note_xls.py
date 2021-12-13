import base64
import pytz, io, base64, datetime
from pytz import timezone
from datetime import timedelta
import logging
from odoo import models, api
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)


class DeliveryNoteXLS(models.AbstractModel):
    _name = 'report.sea_pegasus_delivery_note_report_xls.delivery_note_xls'
    _inherit = 'report.report_xlsx.abstract'

    def get_address_format(self, company):
        address = ""
        if company.street:
            address += company.street + ", "
        if company.street2:
            address += company.street2 + ", "
        if company.city:
            address += company.city + ", "
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
        worksheet1 = workbook.add_worksheet('Delivery Note')
        company_name = self.env.user.company_id.display_name
        company_phone = self.env.user.company_id.phone
        company_mail = self.env.user.company_id.catchall
        company_logo = io.BytesIO(base64.b64decode(self.env.user.company_id.logo))

        f1 = workbook.add_format(
            {'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 18,
             'font_name': 'Times New Roman'})
        f2 = workbook.add_format(
            {'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 10, 'font_name': 'Times New Roman'})
        f3 = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
             'font_name': 'Times New Roman'})
        f4 = workbook.add_format(
            {'bottom': 1, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
             'font_name': 'Times New Roman'})
        f4_1 = workbook.add_format(
            {'bottom': 1, 'right': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
             'font_name': 'Times New Roman'})
        f5 = workbook.add_format(
            {'bold': 1, 'border': 1, 'underline': 1, 'align': 'left', 'valign': 'vcenter',
             'text_wrap': True,
             'font_size': 12, 'font_name': 'Times New Roman'})
        f6 = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
             'font_name': 'Times New Roman'})
        f7 = workbook.add_format(
            {'bold': 1, 'left': 1, 'top': 1, 'bottom': 1, 'underline': 1, 'align': 'left', 'valign': 'vcenter',
             'text_wrap': True,
             'font_size': 12, 'font_name': 'Times New Roman'})
        f8 = workbook.add_format(
            {'italic': 1, 'top': 1, 'right': 1, 'bottom': 1, 'align': 'left',
             'valign': 'vcenter', 'text_wrap': True, 'font_size': 12, 'font_name': 'Times New Roman'})
        f11 = workbook.add_format(
            {'border': 1, 'valign': 'vcenter', 'text_wrap': True, 'num_format': '#,##0', 'font_size': 12,
             'font_name': 'Times New Roman'})
        f12 = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'num_format': '#,##0',
             'font_size': 12,
             'font_name': 'Times New Roman'})
        f13 = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bg_color': '#CCFFFF',
             'font_size': 12, 'font_name': 'Times New Roman'})
        border_short_date = workbook.add_format(
            {'border': 1, 'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'num_format': 'dd/mmm',
             'font_size': 12, 'font_name': 'Times New Roman'})
        border_short_date_alt = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'num_format': 'dd/mmm/yy',
             'font_size': 12, 'font_name': 'Times New Roman'})
        row_no = 0

        # Format column
        worksheet1.set_column(0, 0, 11)
        worksheet1.set_column(1, 1, 14.29)
        worksheet1.set_column(2, 2, 28.43)
        worksheet1.set_column(3, 3, 12.5)
        worksheet1.set_column(4, 4, 11.71)
        worksheet1.set_column(5, 5, 16)
        worksheet1.set_row(1, 21)
        worksheet1.set_row(2, 26)
        worksheet1.set_row(9, 30)
        worksheet1.set_row(12, 30)

        worksheet1.insert_image(0, 0, "company_logo.png",
                                {'image_data': company_logo, 'x_scale': 0.22, 'y_scale': 0.21})
        worksheet1.merge_range(row_no, 4, row_no, 5, _('PM-QT-12.02 (04-01/12/2019)'), f2)
        row_no += 1
        worksheet1.merge_range(row_no, 3, row_no + 1, 5, _('DELIVERY NOTE'), f1)
        row_no += 3

        worksheet1.write(row_no, 0, _('Dispatched Date'), f13)
        worksheet1.write(row_no, 1, _('Mode of Delivery'), f13)
        worksheet1.write(row_no, 2, _('Total of Pages'), f13)
        worksheet1.merge_range(row_no, 3, row_no, 5, _('Delivery Note No.'), f13)
        row_no += 1
        worksheet1.write(row_no, 0, objects.date_done or '', border_short_date_alt)
        worksheet1.write(row_no, 1, _(''), border_short_date_alt)
        worksheet1.write(row_no, 2, _(''), border_short_date_alt)
        if objects.partner_id.sea_business_code:
            worksheet1.write(row_no, 3,
                             str(objects.origin) + '.' + str(
                                 objects.partner_id.sea_business_code), f4)
            worksheet1.merge_range(row_no, 4, row_no, 5, str('/' + objects.scheduled_date.strftime("%Y") + '/BGH-PMD'),
                                   f4_1)
        else:
            worksheet1.write(row_no, 3,
                             str(objects.origin), f4)
            worksheet1.merge_range(row_no, 4, row_no, 5, str('/' + objects.scheduled_date.strftime("%Y") + '/BGH-PMD'),
                                   f4_1)
        row_no += 2

        # To
        worksheet1.merge_range(row_no, 0, row_no + 1, 0, _('Invoice To:'), f5)
        if objects.partner_id.is_company == True:
            worksheet1.merge_range(row_no, 1, row_no + 1, 2, objects.partner_id.name, f3)
        else:
            worksheet1.merge_range(row_no, 1, row_no + 1, 2, objects.partner_id.parent_id.name, f3)
        worksheet1.merge_range(row_no, 3, row_no + 1, 3, _('Delivery To:'), f5)
        if objects.partner_id.is_company == True:
            worksheet1.merge_range(row_no, 4, row_no + 1, 5, objects.partner_id.name, f3)
        else:
            worksheet1.merge_range(row_no, 4, row_no + 1, 5, objects.partner_id.parent_id.name, f3)
        row_no += 2
        worksheet1.write(row_no, 0, _('Add:'), f3)
        worksheet1.merge_range(row_no, 1, row_no, 2, self.get_address_format(objects.partner_id), f11)
        worksheet1.write(row_no, 3, _('Add:'), f3)
        for obj in self.env['sale.order'].search([('name', '=', objects.origin)]):
            if obj.sea_temp_delivery_address:
                worksheet1.merge_range(row_no, 4, row_no, 5, obj.sea_temp_delivery_address, f11)
            else:
                worksheet1.merge_range(row_no, 4, row_no, 5, self.get_address_format(objects.partner_id), f11)
        row_no += 1
        worksheet1.write(row_no, 0, _('Tax Code:'), f3)
        worksheet1.merge_range(row_no, 1, row_no, 2, objects.partner_id.vat or '', f11)
        worksheet1.write(row_no, 3, _('Attn:'), f3)
        for ob in self.env['sale.order'].search([('name', '=', objects.origin)]):
            if ob.sea_temp_contact:
                worksheet1.merge_range(row_no, 4, row_no, 5, ob.sea_temp_contact or '', f11)
            else:
                for obj in self.env['res.partner'].search([('parent_id', '=', objects.partner_id.id)]):
                    if not obj.custom_type_id.name and obj.parent_id and obj.type == 'contact':
                        if obj.name and obj.mobile:
                            worksheet1.merge_range(row_no, 4, row_no, 5, str(obj.name) + ' / ' + str(obj.mobile) or '',
                                                   f11)
                        else:
                            worksheet1.merge_range(row_no, 4, row_no, 5, obj.name or '', f11)
        row_no += 2
        worksheet1.merge_range(row_no, 0, row_no, 1, _("Good's general description:"), f7)
        worksheet1.merge_range(row_no, 2, row_no, 5, _("Nautical Charts & Publications"), f8)
        row_no += 2

        worksheet1.merge_range(row_no, 0, row_no, 2, _("Customer's reference"), f13)
        worksheet1.merge_range(row_no, 3, row_no + 1, 5, _("Pegasus's reference"), f13)
        row_no += 1
        worksheet1.write(row_no, 0, _('Order No.'), f13)
        worksheet1.write(row_no, 1, _('Order Date'), f13)
        worksheet1.write(row_no, 2, _("Ship's name"), f13)
        row_no += 1
        for obj in self.env['sale.order'].search([('name', '=', objects.origin)]):
            worksheet1.write(row_no, 0, obj.sea_customer_po_no or '', border_short_date_alt)
        worksheet1.write(row_no, 1, objects.sale_id.date_order or '', border_short_date)
        for obj in self.env['sale.order'].search([('name', '=', objects.origin)]):
            if obj.sea_ship_partner_id.name:
                worksheet1.write(row_no, 2, obj.sea_ship_partner_id.name or '', border_short_date)
            else:
                if objects.partner_id.is_company == True:
                    worksheet1.write(row_no, 2, objects.partner_id.name, border_short_date)
                else:
                    worksheet1.write(row_no, 2, objects.partner_id.parent_id.name, border_short_date)
        worksheet1.merge_range(row_no, 3, row_no, 5, objects.origin, f6)
        row_no += 2

        # Product
        worksheet1.merge_range(row_no, 0, row_no + 1, 0, _("Line's No."), f13)
        worksheet1.merge_range(row_no, 1, row_no, 2, _("Items"), f13)
        worksheet1.merge_range(row_no, 3, row_no + 1, 3, _("Unit"), f13)
        worksheet1.merge_range(row_no, 4, row_no + 1, 4, _("Qty"), f13)
        worksheet1.merge_range(row_no, 5, row_no + 1, 5, _("Remarks"), f13)
        row_no += 1
        worksheet1.write(row_no, 1, _('Code'), f13)
        worksheet1.write(row_no, 2, _('Description'), f13)
        row_no += 1

        seq = 1
        for move in objects.move_ids_without_package:
            worksheet1.write(row_no, 0, seq, f12)
            seq += 1
            worksheet1.write(row_no, 1, move.product_id.default_code, f12)
            if move.product_id.type == 'service' and move.product_id.categ_id.name == 'Admiralty Vertor Chart Service':
                worksheet1.write(row_no, 2, move.product_id.sea_product_variant_name, f11)
            else:
                worksheet1.write(row_no, 2, move.product_id.name, f11)
            if move.product_uom.name:
                worksheet1.write(row_no, 3, 'Pc', f12)
            worksheet1.write(row_no, 4, move.quantity_done, f12)
            worksheet1.write(row_no, 5, move.remarks, f12)
            row_no += 1
        worksheet1.set_footer(
            'PEGASUS Vietnam -159 Tran Trong Cung, TTD Ward, Dist.7, HCMC-T: 08.37734974 - F: 08.37734972\n'
            'Store/ Acc.                                   Delivery                                  Sale                                   Receiver')
