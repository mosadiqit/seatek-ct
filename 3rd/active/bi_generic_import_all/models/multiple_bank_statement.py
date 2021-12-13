# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


import io
import datetime
import tempfile
import binascii
import logging
from odoo.exceptions import Warning
from odoo import models, fields, api, exceptions, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
_logger = logging.getLogger(__name__)
from io import StringIO

try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')
try:
    import xlwt
except ImportError:
    _logger.debug('Cannot `import xlwt`.')
try:
    import cStringIO
except ImportError:
    _logger.debug('Cannot `import cStringIO`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')
try:
    import xlrd
    from xlrd import XLRDError
except ImportError:
    _logger.debug('Cannot `import xlrd`.')


class AccountMultipleBankStatementWizard(models.TransientModel):
    _name= "account.multiple.bank.statement.wizard"

    file = fields.Binary('File')
    file_opt = fields.Selection([('excel','Excel'),('csv','CSV')])


    @api.multi
    def import_multiple_bank_statement(self):
        if self.file_opt == 'csv':
            try:
                keys = ['name','date','accounting_date','journal_id','line_date','ref','partner','memo','amount','currency']                    
                data = base64.b64decode(self.file)
                file_input = io.StringIO(data.decode("utf-8"))
                file_input.seek(0)
                reader_info = []
                csv_reader = csv.reader(file_input, delimiter=',')
                reader_info.extend(csv_reader)
            except Exception:
                raise Warning(_("Invalid file!"))
            values = {}
            for i in range(len(reader_info)):
                field = list(map(str, reader_info[i]))
                values = dict(zip(keys, field))
                if values:
                    if i == 0:
                        continue
                    else:
                        if values.get('accounting_date') == '':
                            raise Warning('Please Provide Account Date Field Value')
                        if values.get('line_date') == '':
                            raise Warning('Please Provide Line Date Field Value')
                        if values.get('date') == '':
                            raise Warning('Please Provide Date Field Value')

                        res = self.create_bank_statement(values)
                        
        elif self.file_opt == 'excel':
            try:
                fp = tempfile.NamedTemporaryFile(delete= False,suffix=".xlsx")
                fp.write(binascii.a2b_base64(self.file))
                fp.seek(0)
                values = {}
                workbook = ''
                workbook = xlrd.open_workbook(fp.name)
                sheet = workbook.sheet_by_index(0)
            except Exception:
                raise Warning(_("Invalid file!"))
                
            for row_no in range(sheet.nrows):
                if row_no <= 0:
                    fields = list(map(lambda row:row.value.encode('utf-8'), sheet.row(row_no)))
                else:
                    line = list(map(lambda row:isinstance(row.value, str) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))
                    if not line[1]:
                        raise Warning('Please Provide Date Field Value')

                                            
                    statement_date = int(float(line[1]))
                    data_tuple = xlrd.xldate_as_tuple(statement_date, workbook.datemode)
                    date_string = datetime.date(data_tuple[0], data_tuple[1], data_tuple[2])
                    if not line[2]:
                        raise Warning('Please Provide Account Date Field Value')

                    if line[2]:
                        statement_acc_date = int(float(line[2]))
                        statement_acc_date_as_datetime = xlrd.xldate_as_tuple(statement_acc_date, workbook.datemode)
                        acc_date_string = datetime.date(data_tuple[0], data_tuple[1], data_tuple[2])
                        
                    if not line[4]:
                        raise Warning('Please Provide Line Date Field Value')
                                                
                    line_date = int(float(line[4]))
                    line_date_as_datetime = xlrd.xldate_as_tuple(statement_acc_date, workbook.datemode)
                    line_date_string = datetime.date(data_tuple[0], data_tuple[1], data_tuple[2])
                    
                    values.update({
                                    'name' : line[0],
                                    'date' : date_string,
                                    'accounting_date' : acc_date_string,
                                    'journal_id' :  line[3],
                                    'line_date': line_date_string,
                                    'ref': line[5],
                                    'partner': line[6],
                                    'memo': line[7],
                                    'amount': line[8],
                                    'currency' : line[9],
                                    })
                    res = self.create_bank_statement(values)
        else:
            raise Warning('Please Select File Type')

        return res

    @api.multi
    def create_bank_statement(self,values):
        bank_statement_obj = self.env['account.bank.statement']
        
        journal_id = self._find_journal(values.get('journal_id'))
        journal = self.env['account.journal'].browse(journal_id)

        bank_recent_id = bank_statement_obj.search([('journal_id','=',journal.id)],order="id desc", limit=1)
        bank_statement_ids = bank_statement_obj.search([('name', '=', values.get('name'))])
        balance_start = 0.0
        if bank_recent_id:
            new_ = values.get('date')
            new_date = None
            if isinstance(new_,str):
                new_date = datetime.datetime.strptime(new_, DEFAULT_SERVER_DATE_FORMAT).date()
            else:
                new_date = values.get('date')

            if new_date < bank_recent_id.date :
                raise Warning(_('Invalid Dates !!!!.\n Please Enter Valid Dates,\n Dates must be greater than previous entry.'))

        if bank_statement_ids:    
            if bank_statement_ids.journal_id.name == journal.name:
                b = self.create_bank_statement_lines(values, bank_statement_ids)
                bank_statement_ids.write({
                    'balance_end_real' : bank_statement_ids.balance_end
                })
                return bank_statement_ids
            else:
                raise Warning(_('Journal is different for "%s" .\n Please define same.') % values.get('journal_id'))
        else:
            if not values.get('date'):
                raise Warning(_('Please Provide Date Field Value for Bank Statement.'))
            if bank_recent_id:
                balance_start = bank_recent_id.balance_end
            vals = {
                    'name' : values.get('name'),
                    'journal_id' : journal_id,
                    'date' : values.get('date'),
                    'balance_start' : balance_start,
                    'accounting_date' : values.get('accounting_date') or False,
                }

            bank_statement_id = bank_statement_obj.create(vals)
            
            self.create_bank_statement_lines(values, bank_statement_id)
            
        return bank_statement_id
    
    @api.multi
    def create_bank_statement_lines(self,values,bank_statement_id):
        account_bank_statement_line_obj = self.env['account.bank.statement.line']
        partner_id = self._find_partner(values.get('partner'))
        if values.get('currency') != '':
            currency_id = self._find_currency(values.get('currency'))
        else:
            raise Warning(_('Please Provide Currency Value for Bank Statement.'))

        if not values.get('memo'):
            raise Warning('Please Provide Memo Field Value')
        value = {
                    'date':values.get('line_date'),
                    'ref':values.get('ref'),
                    'partner_id':partner_id or False,
                    'name':values.get('memo'),
                    'amount':values.get('amount'),
                    'currency_id':currency_id,
                    'statement_id':bank_statement_id.id,
                    }
        bank_statement_lines = account_bank_statement_line_obj.create(value)
        return True

    def _find_partner(self,name):
        partner_id = self.env['res.partner'].search([('name','=',name)])
        if partner_id:
            return partner_id.id
        else:
            return

    def _find_currency(self,currency):
        currency_id = self.env['res.currency'].search([('name','=',currency)])
        if currency_id:
            return currency_id.id
        else:
            raise Warning(_(' "%s" Currency are not available.') % currency.decode("utf-8"))

    def _find_journal(self,name):
        journal_id = self.env['account.journal'].search([('name','=',name)])
        if journal_id:
            return journal_id.id
        else:
            raise Warning(_(' "%s" Journal is not available.') % (name))
            

