# Copyright 2019 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging, io, base64
from odoo import models

_logger = logging.getLogger(__name__)


class ReportStockCardReportXlsx(models.AbstractModel):
    _name = 'report.sea_stock_card_report.report_stock_card_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):
        self._define_formats(workbook)
        for product in objects.product_ids:
            for ws_params in self._get_ws_params(workbook, data, product):
                ws_name = ws_params.get('ws_name')
                ws_name = self._check_ws_name(ws_name)
                ws = workbook.add_worksheet(ws_name)
                generate_ws_method = getattr(
                    self, ws_params['generate_ws_method'])
                generate_ws_method(
                    workbook, ws, ws_params, data, objects, product)

    def _get_ws_params(self, wb, data, product):
        filter_template = {
            '1_date_from': {
                'header': {
                    'value': 'Từ ngày',
                },
                'data': {
                    'value': self._render('date_from'),
                    'format': self.format_tcell_date_center,
                },
            },
            '2_date_to': {
                'header': {
                    'value': 'Đến ngày',
                },
                'data': {
                    'value': self._render('date_to'),
                    'format': self.format_tcell_date_center,
                },
            },
            '3_location': {
                'header': {
                    'value': 'Kho',
                },
                'data': {
                    'value': self._render('location'),
                    'format': self.format_tcell_center,
                },
            },
            '4_lot': {
                'header': {
                    'value': 'Lot',
                },
                'data': {
                    'value': self._render('lot'),
                    'format': self.format_tcell_center,
                },
            },
        }
        initial_template = {
            '1_ref': {
                'data': {
                    'value': 'Ban đầu',
                    'format': self.format_tcell_center,
                },
                'colspan': 4,
            },
            '2_balance': {
                'data': {
                    'value': self._render('balance'),
                    'format': self.format_tcell_amount_right,
                },
            },
        }
        stock_card_template = {
            '1_date': {
                'header': {
                    'value': 'Ngày',
                },
                'data': {
                    'value': self._render('date'),
                    'format': self.format_tcell_date_left,
                },
                'width': 25,
            },
            '2_reference': {
                'header': {
                    'value': 'Liên quan',
                },
                'data': {
                    'value': self._render('reference'),
                    'format': self.format_tcell_left,
                },
                'width': 25,
            },
            '3_input': {
                'header': {
                    'value': 'Nhập vào',
                },
                'data': {
                    'value': self._render('input'),
                },
                'width': 25,
            },
            '4_output': {
                'header': {
                    'value': 'Xuất ra',
                },
                'data': {
                    'value': self._render('output'),
                },
                'width': 25,
            },
            '5_remarks': {
                'header': {
                    'value': 'Remarks',
                },
                'data': {
                    'value': self._render('remarks'),
                },
                'width': 25,
            },
            '6_balance': {
                'header': {
                    'value': 'Còn lại',
                },
                'data': {
                    'value': self._render('balance'),
                },
                'width': 25,
            },

        }

        ws_params = {
            'ws_name': product.name,
            'generate_ws_method': '_stock_card_report',
            'title': 'Stock Card - {}'.format(product.name),
            'wanted_list_filter': [k for k in sorted(filter_template.keys())],
            'col_specs_filter': filter_template,
            'wanted_list_initial': [k for k in sorted(initial_template.keys())],
            'col_specs_initial': initial_template,
            'wanted_list': [k for k in sorted(stock_card_template.keys())],
            'col_specs': stock_card_template,
        }
        return [ws_params]

    def _stock_card_report(self, wb, ws, ws_params, data, objects, product):
        ws.set_portrait()
        ws.fit_to_pages(1, 0)
        ws.set_header(self.xls_headers['standard'])
        ws.set_footer(self.xls_footers['standard'])
        self._set_column_width(ws, ws_params)

        # Title Company
        company_name = self.env.user.company_id.display_name
        company_street = self.env.user.company_id.street
        company_street2 = self.env.user.company_id.street2
        company_city = self.env.user.company_id.city
        company_country = self.env.user.company_id.country_id.name
        company_phone = self.env.user.company_id.phone
        company_mail = self.env.user.company_id.catchall
        company_logo = io.BytesIO(base64.b64decode(self.env.user.company_id.logo))
        website = self.env.user.company_id.website
        f1 = wb.add_format({'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 24})
        f2 = wb.add_format({'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 10, 'italic': True})
        f3 = wb.add_format({'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        f4 = wb.add_format({'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        f5 = wb.add_format({'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'italic': True})

        ws.insert_image(0, 0, "company_logo.png", {'image_data': company_logo, 'x_scale': 0.19, 'y_scale': 0.17})
        ws.merge_range(0, 1, 0, 12, company_name, f1)
        ws.merge_range(1, 1, 1, 12, ('Địa chỉ: ') + company_street + (', ') + str(company_street2) + (', ') + str(company_city) + (', ') + str(company_country), f2)
        ws.merge_range(2, 1, 2, 12, ('Điện thoại: ') + str(company_phone) + ('     Email: ') + company_mail, f2)
        ws.merge_range(3, 1, 3, 12, website, f2)

        # Title
        row_pos = 7
        row_pos = self._write_ws_title(ws, row_pos, ws_params, True)

        # Filter Table
        row_pos = self._write_line(
            ws, row_pos, ws_params, col_specs_section='header',
            default_format=self.format_theader_blue_center,
            col_specs='col_specs_filter', wanted_list='wanted_list_filter')
        row_pos = self._write_line(
            ws, row_pos, ws_params, col_specs_section='data',
            render_space={
                'date_from': objects.date_from or '',
                'date_to': objects.date_to or '',
                'location': objects.location_id.display_name or '',
                'lot': objects.lot_id.name or ''
            },
            col_specs='col_specs_filter', wanted_list='wanted_list_filter')
        row_pos += 1
        # Stock Card Table
        row_pos = self._write_line(
            ws, row_pos, ws_params, col_specs_section='header',
            default_format=self.format_theader_blue_center)
        ws.freeze_panes(row_pos, 0)
        balance = objects._get_initial(objects.results.filtered(
            lambda l: l.product_id == product and l.is_initial))
        row_pos = self._write_line(
            ws, row_pos, ws_params, col_specs_section='data',
            render_space={'balance': balance}, col_specs='col_specs_initial',
            wanted_list='wanted_list_initial')
        product_lines = objects.results.filtered(
                lambda l: l.product_id == product and not l.is_initial)
        for line in product_lines:
            balance += line.product_in - line.product_out
            row_pos = self._write_line(
                ws, row_pos, ws_params, col_specs_section='data',
                render_space={
                    'date': line.date or '',
                    'reference': line.reference or '',
                    'input': line.product_in or 0,
                    'output': line.product_out or 0,
                    'balance': balance,
                    'remarks': line.remarks or 0
                },
                default_format=self.format_tcell_amount_right)

        # Sign
        row_pos += 1
        ws.merge_range(row_pos, 0,  row_pos, 1, str('____, ____/____/20___'), f3)
        ws.merge_range(row_pos, 4, row_pos, 6, str('____, ____/____/20___'), f3)
        ws.merge_range(row_pos + 1, 0, row_pos + 1, 1, str('Trưởng phòng'), f4)
        ws.merge_range(row_pos + 1, 4, row_pos + 1, 6, str('Người lập'), f4)
        ws.merge_range(row_pos + 2, 0, row_pos + 2, 1, str('(Ký, họ tên)'), f5)
        ws.merge_range(row_pos + 2, 4, row_pos + 2, 6, str('(Ký, họ tên)'), f5)