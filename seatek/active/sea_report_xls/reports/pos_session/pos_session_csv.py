# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import datetime, pytz, csv
from pytz import timezone
from datetime import timedelta


class PosSessionCSV(models.AbstractModel):
    _inherit = 'report.report_csv.abstract'
    _name = 'report.sea_report_xls.pos_session_csv'

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

    def generate_csv_report(self, writer, data, wizard):

        if wizard.type == 'time':
            self.report_time()
        elif wizard.type == 'user':
            self.report_user()
        else:
            objs_order = self.report_session(wizard.session_id)

        writer.fieldnames = [
            'Name',
            'Date Order',
            'Location',
            'State',
        ]

        writer.writeheader()
        for obj in objs_order:
            c = 0
            items_list = {
                    writer.fieldnames[c]: obj.name,
                    writer.fieldnames[c + 1]: obj.date_order,
                    writer.fieldnames[c + 2]: obj.location_id.name,
                    writer.fieldnames[c + 3]: obj.state,
                }
            writer.writerow(items_list)