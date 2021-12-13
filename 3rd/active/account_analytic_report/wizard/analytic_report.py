# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import fields, models, api, _
from datetime import timedelta, datetime, date
from itertools import groupby
from xlwt import *
import xlwt
import base64
import io

def xls_cleanup(text):
    if text:
        return text.encode('ascii', 'ignoer').decode('ascii')
    else:
        return ''


class AccountAnalyticDetails(models.TransientModel):
    _name = 'account.analytic.wizard'
    _description = 'Account Analytic Details Report'

    filter_date = fields.Selection([('current_month', 'Current Month'),
                                    ('current_quarter', 'Current Quarter'),
                                    ('current_fiscal_year', 'Current Fiscal Year'),
                                    ('last_month', 'Last Month'),
                                    ('last_quarter', 'Last Quarter'),
                                    ('last_fiscal_year', 'Last Fiscal Year'),
                                    ('custom', 'Custom')], string="Filter Date", default='current_fiscal_year', required=True)

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)
    date_from = fields.Date(string='Start Date', required=True)
    date_to = fields.Date(string='End Date', required=True)
    analytic_account_ids = fields.Many2many('account.analytic.account', string="Accounts")
    tag_ids = fields.Many2many('account.analytic.tag', string='Tags', copy=True)

    @api.onchange('filter_date')
    def onchange_filter_date(self):
        self.date_from = False
        self.date_to = False
        if self.filter_date and self.filter_date != 'custom':
            today = date.today()
            if self.filter_date == 'current_month':
                dt_from = today.replace(day=1) or False
                dt_to = (today.replace(day=1) + timedelta(days=31)).replace(day=1) - timedelta(days=1)
            elif self.filter_date == 'current_quarter':
                quarter = (today.month - 1) // 3 + 1
                dt_to = (today.replace(month=quarter * 3, day=1) + timedelta(days=31)).replace(day=1) - timedelta(days=1)
                dt_from = dt_to.replace(day=1, month=dt_to.month - 2, year=dt_to.year)
            elif self.filter_date == 'current_fiscal_year':
                company_fiscalyear_dates = self.env.user.company_id.compute_fiscalyear_dates(today)
                dt_from = company_fiscalyear_dates.get('date_from') or False
                dt_to = company_fiscalyear_dates.get('date_to') or False
            elif self.filter_date == 'last_month':
                dt_to = today.replace(day=1) - timedelta(days=1)
                dt_from = dt_to.replace(day=1) or False
            elif self.filter_date == 'last_quarter':
                quarter = (today.month - 1) // 3 + 1
                quarter = quarter - 1 if quarter > 1 else 4
                dt_to = (today.replace(month=quarter * 3, day=1, year=today.year if quarter != 4 else today.year - 1) + timedelta(days=31)).replace(day=1) - timedelta(days=1)
                dt_from = dt_to.replace(day=1, month=dt_to.month - 2, year=dt_to.year) or False
            elif self.filter_date == 'last_fiscal_year':
                company_fiscalyear_dates = self.env.user.company_id.compute_fiscalyear_dates(today.replace(year=today.year - 1))
                dt_from = company_fiscalyear_dates.get('date_from') or False
                dt_to = company_fiscalyear_dates.get('date_to')
            self.date_from = dt_from
            self.date_to = dt_to

    @api.multi
    def get_acc_analytic_lines(self):
        domain = []
        if self.analytic_account_ids:
            domain += [('id', 'in', self.analytic_account_ids.ids)]
        if self.company_id:
            domain += [('company_id', '=', self.company_id.id)]
        analytic_accounts = self.env['account.analytic.account'].sudo().search(domain)
        if self.tag_ids:
            analytic_lines = analytic_accounts.mapped('line_ids').filtered(lambda f: f.date >= self.date_from and f.date <= self.date_to).filtered(lambda l: set(l.tag_ids.ids) & set(self.tag_ids.ids)).ids
        else:
            analytic_lines = analytic_accounts.mapped('line_ids').filtered(lambda f: f.date >= self.date_from and f.date <= self.date_to).ids

        form_view = self.env.ref('analytic.view_account_analytic_line_form')
        tree_view  = self.env.ref('analytic.view_account_analytic_line_tree')
        return {
            'name': 'Analytic Lines',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.analytic.line',
            'views': [(tree_view.id,'tree'), (form_view.id, 'form')],
            'domain': [('id', 'in', analytic_lines)],
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': {'group_by': 'account_id'},
            'nodestroy': True,
        }

    @api.model
    def _get_report_lines(self, line_id=None):
        AccountAnalyticGroup = self.env['account.analytic.group']

        analytic_domain = []
        if self.analytic_account_ids:
            analytic_domain += [('id', 'in', self.analytic_account_ids.ids)]
        if self.company_id:
            analytic_domain += [('company_id', '=', self.company_id.id)]

        account_analytic_ids = self.env['account.analytic.account'].search(analytic_domain)
        parent_group_ids = AccountAnalyticGroup.search([('parent_id', '=', False)])
        lines = []
        for group in parent_group_ids:
            lines.append({'name': group.name, 'id': group.id, 'children_ids': [child for child in group.children_ids]})
        return lines

    @api.multi
    def generate_pdf_report(self):
        lines = self._get_report_lines()
        data = {'date_from': self.date_from, 'date_to': self.date_to, "data":lines, 'analytic_accounts': self.analytic_account_ids.ids, 'acc_company': self.company_id.id, 'acc_tags': self.tag_ids.ids}
        return self.env.ref('account_analytic_report.report_analytic').report_action([], data=data)

    @api.multi
    def generate_xml_report(self):
        context = dict(self.env.context) or {}
        parent_group_ids = self._get_report_lines()

        date_alignment = xlwt.Alignment()
        date_alignment.horz = xlwt.Alignment.HORZ_LEFT

        date_format = xlwt.XFStyle()
        date_format.num_format_str = 'dd/mm/yyyy'
        date_format.alignment = date_alignment

        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Worksheet', cell_overwrite_ok=True)
        worksheet.set_portrait(False)

        currency_format = xlwt.XFStyle()
        currency_format.num_format_str = '%s#,##0.00' % (self.company_id.currency_id.symbol)

        title_alignment = xlwt.Alignment()
        title_alignment.horz = xlwt.Alignment.HORZ_CENTER
        title_alignment.vert = xlwt.Alignment.VERT_CENTER

        wrap_style = xlwt.XFStyle()
        wrap_style.alignment.wrap = 1

        amount_alignment = xlwt.Alignment()
        amount_alignment.horz = xlwt.Alignment.HORZ_RIGHT

        worksheet.row(0).height_mismatch = True
        worksheet.row(0).height = 20*36

        header_style = xlwt.easyxf('font: bold 1, name Verdana, height 360, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black;\
                     pattern: pattern solid, fore_color white;')
        header_style.alignment = title_alignment

        tbl_head_sty = xlwt.easyxf('font: bold 1, name Verdana, height 220, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black; pattern: fore_color white;')
        tbl_head_sty.alignment = title_alignment

        bold_sty = xlwt.easyxf('font: bold 1, name Verdana, height 200, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black;\
                     pattern: fore_color white;')

        parent_group_sty = xlwt.easyxf('font: bold 1, name Verdana, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black;\
                     pattern: fore_color white;')
        parent_group_amt_sty = xlwt.easyxf('font: bold 1, name Verdana, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black;\
                     pattern: fore_color white;')
        parent_group_amt_sty.alignment = amount_alignment

        child_group_amt_sty = xlwt.easyxf('font: bold 0, name Verdana, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black;\
                     pattern: fore_color white;')
        child_group_amt_sty.alignment = amount_alignment

        i = 0
        row = 0
        for rec in self:
            i += 1
            worksheet.col(0).width = 6000
            worksheet.col(1).width = 6000
            worksheet.col(2).width = 6000
            worksheet.col(3).width = 6000
            worksheet.col(4).width = 6000

            analytic_names = ', '.join(rec.analytic_account_ids.mapped('name'))
            tag_names = ', '.join(rec.tag_ids.mapped('name'))

            worksheet.row(row).height = 20*36
            worksheet.write_merge(row, row, 0, 4, "Analytic Report", header_style)

            row += 1
            worksheet.row(row).height = 280
            worksheet.write_merge(row, row, 0, 4, " ")

            row += 1
            worksheet.row(row).height = 280
            worksheet.write(row, 0, "Start Date: ", bold_sty)
            worksheet.write(row, 1, "End Date: ", bold_sty)
            worksheet.write(row, 2, "Companies: ", bold_sty)
            worksheet.write(row, 3, "Analytic Accounts: ", bold_sty)
            worksheet.write(row, 4, "Analytic Tags: ", bold_sty)
            
            row += 1
            worksheet.row(row).height = 280
            worksheet.write(row, 0, rec.date_from, date_format)
            worksheet.write(row, 1, rec.date_to, date_format)
            worksheet.write(row, 2, rec.company_id.name)
            worksheet.write(row, 3, (analytic_names if analytic_names else 'All'), wrap_style)
            worksheet.write(row, 4, (tag_names if tag_names else 'All'), wrap_style)
            
            title = [
                '',
                '',
                'Reference',
                'Partner',
                'Balance',
            ]
            row += 1
            worksheet.row(row).height = 280
            worksheet.write_merge(row, row, 0, 4, " ")

            row += 1
            for i, fieldname in enumerate(title):
                worksheet.row(row).height = 280
                worksheet.write(row, i, fieldname, tbl_head_sty)
            worksheet.write_merge(row, row, 0, 1, " ", tbl_head_sty)
            
            row += 1
            c = 5
            for parent in parent_group_ids:
                analytic_accounts = self.env['account.analytic.account'].sudo().get_analytic_account(parent.get('id'), rec.date_from, rec.date_to, rec.analytic_account_ids.ids, rec.company_id.id)
                analytic_balance = []
                if parent:
                    all_analytic_account = self.env['account.analytic.account'].with_context(all_group=True).sudo().get_analytic_account(parent.get('id'), rec.date_from, rec.date_to, rec.analytic_account_ids.ids, rec.company_id.id)
                    if rec.tag_ids:
                        analytic_balance = all_analytic_account.mapped('line_ids').filtered(lambda f: f.date >= rec.date_from and f.date <= rec.date_to).filtered(lambda l: set(l.tag_ids.ids) & set(rec.tag_ids.ids)).mapped('amount')
                    else:
                        analytic_balance = all_analytic_account.mapped('line_ids').filtered(lambda f: f.date >= rec.date_from and f.date <= rec.date_to).mapped('amount')

                parent_id = self.env['account.analytic.group'].browse(parent.get('id'))
                worksheet.row(row).height = 280
                worksheet.write_merge(row, row, 0, 1, xls_cleanup(parent_id.name), parent_group_sty)
                worksheet.write(row, 2, '', parent_group_sty)
                worksheet.write(row, 3, '', parent_group_sty)
                worksheet.write(row, 4, (str(rec.company_id.currency_id.symbol) if rec.company_id.currency_id else '') + str(float(sum(analytic_balance))), parent_group_amt_sty)
                row += 1

                for analytic_account in analytic_accounts:
                    if rec.tag_ids:
                        analytic_account_balance = analytic_account.mapped('line_ids').filtered(lambda f: f.date >= rec.date_from and f.date <= rec.date_to).filtered(lambda l: set(l.tag_ids.ids) & set(rec.tag_ids.ids)).mapped('amount')
                    else:
                        analytic_account_balance = analytic_account.mapped('line_ids').filtered(lambda f: f.date >= rec.date_from and f.date <= rec.date_to).mapped('amount')
                    analytic_lines = self.env['account.analytic.line']._get_analytic_lines(analytic_account, rec.date_from, rec.date_to, rec.company_id.id, rec.tag_ids.ids)
                    worksheet.row(row).height = 280
                    worksheet.write_merge(row, row, 0, 1, xls_cleanup(analytic_account.name))
                    worksheet.write(row, 2, xls_cleanup(analytic_account.code))
                    worksheet.write(row, 3, (xls_cleanup(analytic_account.partner_id.name) if analytic_account.partner_id else ''))
                    worksheet.write(row, 4, (str(analytic_account.currency_id.symbol) if analytic_account.currency_id else '') + str(float(sum(analytic_account_balance))), child_group_amt_sty)
                    row += 1

                children_ids = parent_id.children_ids
                space = "     "
                while len(children_ids) >= 1:
                    for children in children_ids:
                        child_analytic_accs = self.env['account.analytic.account'].sudo().get_analytic_account(children.id, rec.date_from, rec.date_to, rec.analytic_account_ids.ids, rec.company_id.id)
                        child_analytic_bals = []
                        if children:
                            all_child_analytic_accs = self.env['account.analytic.account'].with_context(all_group=True).sudo().get_analytic_account(children.id, rec.date_from, rec.date_to, rec.analytic_account_ids.ids, rec.company_id.id)
                            if rec.tag_ids:
                                child_analytic_bals = all_child_analytic_accs.mapped('line_ids').filtered(lambda f: f.date >= rec.date_from and f.date <= rec.date_to).filtered(lambda l: set(l.tag_ids.ids) & set(rec.tag_ids.ids)).mapped('amount')
                            else:
                                child_analytic_bals = all_child_analytic_accs.mapped('line_ids').filtered(lambda f: f.date >= rec.date_from and f.date <= rec.date_to).mapped('amount')
                        worksheet.row(row).height = 280
                        worksheet.write_merge(row, row, 0, 1, space + xls_cleanup(children.name), parent_group_sty)
                        worksheet.write(row, 2, '')
                        worksheet.write(row, 3, '')
                        worksheet.write(row, 4, (str(rec.company_id.currency_id.symbol) if rec.company_id.currency_id else '') + str(float(sum(child_analytic_bals))), parent_group_amt_sty)
                        row += 1
                        for child_analytic_acc in child_analytic_accs:
                            if rec.tag_ids:
                                child_analytic_acc_balance = child_analytic_acc.mapped('line_ids').filtered(lambda f: f.date >= rec.date_from and f.date <= rec.date_to).filtered(lambda l: set(l.tag_ids.ids) & set(rec.tag_ids.ids)).mapped('amount')
                            else:
                                child_analytic_acc_balance = child_analytic_acc.mapped('line_ids').filtered(lambda f: f.date >= rec.date_from and f.date <= rec.date_to).mapped('amount')
                            child_analytic_lines = self.env['account.analytic.line']._get_analytic_lines(child_analytic_acc, rec.date_from, rec.date_to, rec.company_id.id, rec.tag_ids.ids)
                            worksheet.row(row).height = 280
                            worksheet.write_merge(row, row, 0, 1, space + xls_cleanup(child_analytic_acc.name))
                            worksheet.write(row, 2, xls_cleanup(child_analytic_acc.code))
                            worksheet.write(row, 3, (xls_cleanup(child_analytic_acc.partner_id.name) if child_analytic_acc.partner_id else ''))
                            worksheet.write(row, 4, (str(child_analytic_acc.currency_id.symbol) if child_analytic_acc.currency_id else '') + str(float(sum(child_analytic_acc_balance))), child_group_amt_sty)
                            row += 1
                        if children.children_ids:
                            children_ids = children.children_ids
                            space += "     "
                        else:
                            children_ids = []

            accounts_wo_groups = self.env['account.analytic.account'].sudo().get_analytic_account('', rec.date_from, rec.date_to, rec.analytic_account_ids.ids, rec.company_id.id)
            if accounts_wo_groups:
                acc_wo_grp_balance = []
                if rec.tag_ids:
                    acc_wo_grp_balance = accounts_wo_groups.mapped('line_ids').filtered(lambda l: set(l.tag_ids.ids) & set(rec.tag_ids.ids)).mapped('account_id').mapped('balance')
                else:
                    acc_wo_grp_balance = accounts_wo_groups.mapped('balance')

                worksheet.row(row).height = 280
                worksheet.write_merge(row, row, 0, 1, "Accounts without a group", parent_group_sty)
                worksheet.write(row, 2, '', parent_group_sty)
                worksheet.write(row, 3, '', parent_group_sty)
                worksheet.write(row, 4, (str(rec.company_id.currency_id.symbol) if rec.company_id.currency_id else '') + str(sum(acc_wo_grp_balance)), parent_group_amt_sty)
                row += 1

                for accounts_wo_group in accounts_wo_groups:
                    accounts_wo_group_balance = accounts_wo_group.mapped('line_ids').filtered(lambda f: f.date >= self.date_from and f.date <= self.date_to).mapped('account_id').mapped('balance')
                    analytic_lines_wo_grps = self.env['account.analytic.line']._get_analytic_lines(accounts_wo_group, rec.date_from, rec.date_to, rec.company_id.id, rec.tag_ids.ids)
                    worksheet.row(row).height = 280
                    worksheet.write_merge(row, row, 0, 1, xls_cleanup(accounts_wo_group.name))
                    worksheet.write(row, 2, xls_cleanup(accounts_wo_group.code))
                    worksheet.write(row, 3, (xls_cleanup(accounts_wo_group.partner_id.name) if accounts_wo_group.partner_id else ''))
                    worksheet.write(row, 4, (str(accounts_wo_group.currency_id.symbol) if accounts_wo_group.currency_id else '') + str(float(sum(accounts_wo_group_balance))), child_group_amt_sty)
                    row += 1

        fp = io.BytesIO()
        workbook.save(fp)
        fp.seek(0)
        data_of_file = fp.read()
        fp.close()
        file_name = '%s.xls' % ("Analytic Report")
        file_save = base64.encodestring(data_of_file)
        attachment_id = self.env['ir.attachment'].create({
                                                    'name': file_name,
                                                    'datas': file_save,
                                                    'datas_fname': file_name,
                                                    'res_model': 'account.analytic.wizard',
                                                    'res_id': self.id,
                                                    'type': 'binary',
                                                })
        config_id = self.env['ir.config_parameter'].sudo().search([('key', '=', 'web.base.url')], limit=1)
        if attachment_id and config_id:
            return {
                'type': 'ir.actions.act_url',
                'url': '%s/web/content/%s?download=true' % (config_id.value, attachment_id.id),
                'target': 'self',
                'nodestroy': False,
                'context': context
            }
