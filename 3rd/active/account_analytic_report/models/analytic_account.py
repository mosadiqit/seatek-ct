# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class AccountAnalyticGroup(models.Model):
    _inherit = 'account.analytic.group'

    @api.model
    def get_children(self, group_id):
        group_id = self.browse(group_id)
        if group_id and group_id.children_ids:
            return group_id.children_ids


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.model
    def get_analytic_account(self, group_id, date_from, date_to, analytic_acc, company_id):
        date_from = datetime.strptime(str(date_from),DEFAULT_SERVER_DATE_FORMAT).date()
        date_to = datetime.strptime(str(date_to),DEFAULT_SERVER_DATE_FORMAT).date()
        domain = []
        group = self.env['account.analytic.group'].browse(group_id).name
        if self._context.get('all_group') and group_id:
            domain += [('group_id', 'child_of', group_id)]
        elif group_id:
            domain += [('group_id', '=', group_id)]
        else:
            domain += [('group_id', '=', False)]
        if analytic_acc:
            domain += [('id', 'in', analytic_acc)]
        if company_id:
            domain += [('company_id', '=', company_id)]
        accounts = self.sudo().search(domain)
        return accounts

    @api.multi
    def get_analytic_account_balance(self, accounts, acc_tags, date_from, date_to):
        date_from = datetime.strptime(str(date_from),DEFAULT_SERVER_DATE_FORMAT).date()
        date_to = datetime.strptime(str(date_to),DEFAULT_SERVER_DATE_FORMAT).date()
        tag_ids = self.env['account.analytic.tag'].browse(acc_tags)
        balance = []
        if tag_ids:
            balance = accounts.mapped('line_ids').filtered(lambda f: f.date >= date_from and f.date <= date_to).filtered(lambda l: set(l.tag_ids.ids) & set(tag_ids.ids)).mapped('amount')
        else:
            balance = accounts.mapped('line_ids').filtered(lambda f: f.date >= date_from and f.date <= date_to).mapped('amount')
        return sum(balance)

    @api.model
    def get_analytic_account_name(self, analytic_acc):
        accounts = self.browse(analytic_acc)
        account_name = []
        for account in accounts:
            account_name.append(account.name)
        return account_name

    @api.model
    def get_analytic_tags_name(self, acc_tags):
        tag_ids = self.env['account.analytic.tag'].browse(acc_tags)
        tag_name = []
        for tag in tag_ids:
            tag_name.append(tag.name)
        return tag_name


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    @api.model
    def _get_analytic_lines(self, account, date_from, date_to, company_id, tags):
        date_from = datetime.strptime(str(date_from),DEFAULT_SERVER_DATE_FORMAT).date()
        date_to = datetime.strptime(str(date_to),DEFAULT_SERVER_DATE_FORMAT).date()
        domain = []
        if account:
            domain += [('account_id', '=', account.id)]
        if date_from:
            domain += [('date', '>=', date_from)]
        if date_to:
            domain += [('date', '<=', date_to)]
        if company_id:
            domain += [('company_id', '=', company_id)]
        if tags:
            domain += [('tag_ids', 'in', tags)]
        analytic_lines = self.sudo().search(domain)
        return analytic_lines
