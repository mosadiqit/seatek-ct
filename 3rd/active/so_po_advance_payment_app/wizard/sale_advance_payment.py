# -*- coding: utf-8 -*-

from odoo import models,fields,api,_
from odoo.exceptions import Warning

class SaleAdvancePayment(models.TransientModel):
    _name = 'sale.advance.payment'
    _description = "Sale Advance Payment"

    sale_order_id = fields.Many2one('sale.order', string="Name")
    journal_id = fields.Many2one('account.journal', string="Payment (Journal)")
    name = fields.Char(string="Origin", readonly=True)
    payment_date = fields.Datetime(string="Payment Date")
    total_amount = fields.Float(string="Total Amount", readonly=True)
    advance_amount = fields.Float(string="Advance Pay Amount", required=True)
    currency_id = fields.Many2one('res.currency', string="Payment Currency", readonly=True)
    currency_rate = fields.Float(string="Currency Rate", readonly=True)
    company_id = fields.Many2one('res.company', string="Company")
    partner_id = fields.Many2one('res.partner', string="Partner")
    payment_method_id = fields.Many2one('account.payment.method', string='Payment Method', required=True, oldname="payment_method",
        help="Manual: Get paid by cash, check or any other method outside of Odoo.\n"\
        "Electronic: Get paid automatically through a payment acquirer by requesting a transaction on a card saved by the customer when buying or subscribing online (payment token).\n"\
        "Check: Pay bill by check and print it from Odoo.\n"\
        "Batch Deposit: Encase several customer checks at once by generating a batch deposit to submit to your bank. When encoding the bank statement in Odoo, you are suggested to reconcile the transaction with the batch deposit.To enable batch deposit, module account_batch_payment must be installed.\n"\
        "SEPA Credit Transfer: Pay bill from a SEPA Credit Transfer file you submit to your bank. To enable sepa credit transfer, module account_sepa must be installed ")

    @api.model
    def default_get(self,default_fields):
        res = super(SaleAdvancePayment, self).default_get(default_fields)
        context = self._context
        payment_data = {'name':context.get('name'), 'currency_id':context.get('currency_id'), 'total_amount':context.get('total_amount'), 'currency_rate':context.get('currency_rate'), 'payment_date':context.get('date_order'), 'company_id':context.get('company_id'), 'sale_order_id':context.get('order_id'), 'partner_id':context.get('partner_id'), 'journal_id':self.env['account.journal'].search([],limit=1).id, 'payment_method_id':self.env['account.payment.method'].search([],limit=1).id}
        res.update(payment_data)
        return res

    @api.multi
    def gen_purchase_advance_payment(self):
        if self.total_amount < self.advance_amount or self.advance_amount == 0.00:
            raise Warning(_('Please enter valid advance payment amount..!'))

        payment_obj = self.env['account.payment']
        payment_data = {'payment_type':'inbound', 'partner_type':'customer', 'partner_id':self.partner_id.id, 'amount':self.advance_amount, 'journal_id':self.journal_id.id, 'payment_date':self.payment_date, 'communication':self.sale_order_id.name,'payment_method_id':self.payment_method_id.id}
        res = payment_obj.create(payment_data)
        res.post()
        self.write({'name':res.name})               
        
        self.sale_order_id.write({'payment_history_ids':[(0,0,{'name':self.name, 'payment_date':self.payment_date, 'partner_id':self.partner_id.id, 'journal_id':self.journal_id.id, 'payment_method_id':self.payment_method_id.id, 'currency_id':self.currency_id.id, 'currency_rate':self.currency_rate, 'advance_amount':self.advance_amount, 'total_amount':self.total_amount})]})

        action_vals = {
            'name': _('Advance Payment'),
            'domain': [('id', 'in', res.ids), ('state', '=', 'posted')],
            'view_type': 'form',
            'res_model': 'account.payment',
            'view_id': False,
            'type': 'ir.actions.act_window',
        }

        if len(res) == 1:
            action_vals.update({'res_id': res[0].id, 'view_mode': 'form'})
        return action_vals


# Advance Payment History
class AdvancePaymentHistory(models.Model):
    _name = 'advance.payment.history'
    _description = 'advance.payment.history'

    name = fields.Char(string="Name", readonly=True)
    order_id = fields.Many2one('sale.order', string="Sale Order")
    journal_id = fields.Many2one('account.journal', string="Payment (Journal)", readonly=True)
    payment_date = fields.Datetime(string="Payment Date", readonly=True)
    total_amount = fields.Float(string="Total Amount", readonly=True)
    advance_amount = fields.Float(string="Advance Paid Amount", readonly=True)
    currency_id = fields.Many2one('res.currency', string="Payment Currency", readonly=True)
    currency_rate = fields.Float(string="Currency Rate", readonly=True)
    partner_id = fields.Many2one('res.partner', string="Partner")
    payment_method_id = fields.Many2one('account.payment.method', string="Payment Method", readonly=True)