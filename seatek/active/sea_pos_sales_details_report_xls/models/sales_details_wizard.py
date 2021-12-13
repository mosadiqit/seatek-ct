# -*- coding: utf-8 -*-
import datetime
from datetime import timedelta
from odoo import models, fields, api


class PosSalesDetails(models.TransientModel):
    _name = 'pos.sales.details.wizard'

    start_date = fields.Datetime(string='Date From', default=fields.Datetime.now() - timedelta(days=1))
    end_date = fields.Datetime(string='Date To', default=fields.Datetime.now())
    pos_config_ids = fields.Many2many('pos.config', 'pos_sales_details_configs',
                                      default=lambda s: s.env['pos.config'].search([]))

    @api.onchange('start_date')
    def _onchange_start_date(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            self.end_date = self.start_date

    @api.onchange('end_date')
    def _onchange_end_date(self):
        if self.end_date and self.end_date < self.start_date:
            self.start_date = self.end_date

    # Action report PDF
    def button_export_pdf(self):
        datas = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'config_ids': self.pos_config_ids.ids
        }
        return self.env.ref('sea_pos_sales_details_report_xls.action_sales_details_report_pdf').report_action(self,
                                                                                                              data=datas)

    # Action report XLSX
    def button_export_xlsx(self):
        start_date = datetime.datetime(year=self.start_date.year, month=self.start_date.month, day=self.start_date.day,
                                       hour=0, minute=0, second=0)
        end_date = datetime.datetime(year=self.end_date.year, month=self.end_date.month, day=self.end_date.day, hour=23,
                                     minute=59, second=59)
        data = {
            'start_date': start_date,
            'end_date': end_date,
            'config_ids': self.pos_config_ids.ids
        }
        return self.env.ref('sea_pos_sales_details_report_xls.action_sales_details_report_xlsx').report_action(self,
                                                                                                               data=data)

    def button_export_xlsx_by_date(self):
        start_date = datetime.datetime(year=self.start_date.year, month=self.start_date.month, day=self.start_date.day,
                                       hour=0, minute=0, second=0)
        end_date = datetime.datetime(year=self.end_date.year, month=self.end_date.month, day=self.end_date.day, hour=23,
                                     minute=59, second=59)
        data = {
            'start_date': start_date,
            'end_date': end_date,
            'config_ids': self.pos_config_ids.ids
        }
        return self.env.ref('sea_pos_sales_details_report_xls.action_sales_details_by_date').report_action(self,
                                                                                                               data=data)
