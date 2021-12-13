# -*- coding: utf-8 -*-
import pytz
from pytz import timezone
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, exceptions, _
from odoo.fields import Datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import ValidationError


class WizardSaleReport(models.TransientModel):
    _name = 'sea_report_xls.sale_order.wizard'

    date_from = fields.Datetime(string='Date From', default=fields.Datetime.now() - timedelta(days=1))
    date_to = fields.Datetime(string='Date To', default=fields.Datetime.now())
    type = fields.Selection([
                ('by_effective', 'Effective date'),
                ('by_commitment', 'Commitment date'),
                ('by_order_date', 'Order date'),
                ('by_create_date', 'Create date'),
                ], string='Type', required=1, default='by_effective')
    invoice_status = fields.Selection([
                ('upselling', 'Upselling Opportunity'),
                ('invoiced', 'Fully Invoiced'),
                ('to invoice', 'To Invoice'),
                ('no', 'Nothing to Invoice')
                ], string='Invoice Status')
    team_ids = fields.Many2many('crm.team', 'report_sale_order_xls_sale_team_rel', 'wizard_id', 'team_id', 'Sales Team')
    warehouse_ids = fields.Many2many('stock.warehouse', 'report_sale_order_xls_warehouse_rel', 'wizard_id', 'warehouse_id', 'Warehouse')

    @api.constrains('date_from', 'date_to')
    def _constrain_dates(self):
        for rec in self:
            if rec.date_from > rec.date_to:
                raise ValidationError(_('Date From must be greater than date To!'))

    # @api.model
    # def conver_timezone(self, var):
    #     user = self.env["res.users"].browse(self._uid)
    #     tz = timezone(user.tz)
    #     c_time = datetime.datetime.now(tz)
    #     hour_tz = int(str(c_time)[-5:][:2])
    #     min_tz = int(str(c_time)[-5:][3:])
    #     sign = str(c_time)[-6][:1]
    #     if sign == '+':
    #         var_time = datetime.datetime.strptime(str(var), DEFAULT_SERVER_DATETIME_FORMAT) - timedelta(hours=hour_tz, minutes=min_tz)
    #     else:
    #         var_time = datetime.datetime.strptime(str(var), DEFAULT_SERVER_DATETIME_FORMAT) + timedelta(hours=hour_tz, minutes=min_tz)
    #     return str(var_time)

    @api.multi
    def find_objs(self):
        # date_from = datetime.datetime(year=self.date_from.year, month=self.date_from.month, day=self.date_from.day, hour=00, minute=0, second=0)
        # date_to = datetime.datetime(year=self.date_to.year, month=self.date_to.month, day=self.date_to.day, hour=23,
        #                             minute=59, second=59)
        dt_from = Datetime.context_timestamp(self, self.date_from).replace(hour=0, minute=0, second=0)
        dt_from = dt_from.astimezone(pytz.utc)
        dt_from = dt_from.replace(tzinfo=None)
        dt_to = Datetime.context_timestamp(self, self.date_to).replace(minute=59, hour=23, second=59)
        dt_to = dt_to.astimezone(pytz.utc)
        dt_to = dt_to.replace(tzinfo=None)

        search_objs = [('state', '=', ('sale', 'done'))]
        search_invoice = ('invoice_status', '=', self.invoice_status)
        search_team = ('team_id.id', '=', self.team_ids.ids)
        search_warehouse = ('warehouse_id.id', 'in', self.warehouse_ids.ids)
        search_create_date = ['&',('create_date', '>=', dt_from), ('create_date', '<=', dt_to)]
        search_order_date = ['&',('confirmation_date', '>=', dt_from), ('confirmation_date', '<=', dt_to)]
        search_commitment = ['&',('commitment_date', '>=', dt_from), ('commitment_date', '<=', dt_to)]
        search_effective = ['&',('effective_date', '>=', self.date_from), ('effective_date', '<=', self.date_to)]
        if self.invoice_status:
            search_objs.append(search_invoice)
        else:
            search_objs.append(('state', '=', ('sale', 'done')))
        if self.team_ids:
            search_objs.append(search_team)
        if self.warehouse_ids:
            search_objs.append(search_warehouse)
        if self.type == 'by_order_date':
            objs_search = self.env['sale.order'].search(search_objs + search_order_date)
        elif self.type == 'by_commitment':
            objs_search = self.env['sale.order'].search(search_objs + search_commitment)
        elif self.type == 'by_effective':
            objs_search = self.env['sale.order'].search(search_objs + search_effective)
        else:
            objs_search = self.env['sale.order'].search(search_objs + search_create_date)
        if not objs_search:
                raise ValidationError(_('The period choose has no data to report! Please select a different time period.'))
        else:
            return objs_search

    @api.multi
    def view_report(self):
        self.ensure_one()
        if not self.env.user.tz:
                raise ValidationError(_('Please contact Administrator to configure your time zone!!!'))
        else:
            data = self.read()[0]
            objs_sale = self.find_objs()
            datas = {
                'ids': objs_sale.ids,
                'model': 'sale.order',
                'form': data,
                'warehouse': self.warehouse_ids.ids
            }
            return self.env['ir.actions.report'].search(
                [('report_name', '=', 'sea_report_xls.sale_order_xls'),
                ('report_type', '=', 'xlsx')],
                limit=1).report_action(self, data=datas)
