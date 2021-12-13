from datetime import datetime

from odoo import models, fields, api

num = {
    "0": "không",
    "1": "một",
    "2": "hai",
    "3": "ba",
    "4": "bốn",
    "5": "năm",
    "6": "sáu",
    "7": "bảy",
    "8": "tám",
    "9": "chín",
}
ten = {
    "00": "không mươi",
    "01": "lẻ một",
    "02": "lẻ hai",
    "03": "lẻ ba",
    "04": "lẻ bốn",
    "05": "lẻ lăm",
    "06": "lẻ sáu",
    "07": "lẻ bảy",
    "08": "lẻ tám",
    "09": "lẻ chín",
    "10": "mười",
    "11": "mười một",
    "12": "mười hai",
    "13": "mười ba",
    "14": "mười bốn",
    "15": "mười lăm",
    "16": "mười sáu",
    "17": "mười bảy",
    "18": "mười tám",
    "19": "mười chín"
}

greaters = {
    2: "nghìn",
    3: "triệu",
    4: "tỷ",
}


def readGreater(l):
    x = l
    if x <= 3:
        return 0, ""
    # elif x == 2:
    #     return "mươi"
    # elif x == 3:
    #     return "trăm"
    m = 0
    while x > 3:
        m = x % 3
        x = x // 3
        if x == 4:
            break

    if x != 4 and m > 0:
        x += 1
    return x, greaters[x]


def read3Num(s):
    if s == "000":
        return num["0"]
    l = len(s)
    if l == 0:
        return ""
    elif l == 1:
        return num[s]
    elif l == 2:
        if int(s) < 20:
            return ten[s]
        else:
            x = "mươi"
            if s[1] != "0":
                x += " " + num[s[1]]
            return num[s[0]] + " " + x
    else:
        x = num[s[0]] + " trăm"
        s1 = s[1] + s[2]
        if s1 == "00":
            return x
        x += " " + read3Num(s[1] + s[2])
        return x


def readFreeNum(x):
    s = str(x)
    print(s)
    l = len(s)
    mod = l % 3
    count = l // 3
    kq = ""
    if mod == 1:
        x, greater = readGreater(l)
        num3 = num[s[0]]
        kq += " " + num3 + " " + greater
    elif mod == 2:
        x, greater = readGreater(l)
        num3 = read3Num(s[0] + s[1])
        kq += " " + num3 + " " + greater

    l = l - mod
    s = s[mod:]
    if mod > 0 and s.replace('0', '') == "":
        return kq
    for c in range(0, count):
        s1 = s[0]
        s2 = s[1]
        s3 = s[2]
        x, greater = readGreater(l)
        num3 = read3Num(s1 + s2 + s3)
        if x == 4 and num3 == num["0"]:
            kq += " " + greater
        else:
            kq += " " + num3 + " " + greater
        l -= 3
        s = s[3:]
        if l > 0 and s.replace('0', '') == "":
            return kq
    return kq


class PaymentRequest(models.TransientModel):
    _name = "purchase.payment.request"
    _description = 'Đề nghị thanh toán'

    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }

    content = fields.Text('Nội dung')
    purchase_id = fields.Many2one('purchase.order', string='Đơn đặt hàng')
    invoice_ids = fields.One2many('account.invoice', compute="_compute_invoice", string='Danh sách hóa đơn',
                                  domain=[('state', '=', 'open')])
    invoice_ids_paid = fields.One2many('account.invoice', compute="_compute_invoice", string='Bills',
                                       domain=['|', ('state', '=', 'paid'), ('state', '=', 'in_payment')])
    currency_id = fields.Many2one('res.currency', 'Currency', required=True, states=READONLY_STATES,
                                  default=lambda self: self.env.user.company_id.currency_id.id,
                                  compute="_compute_invoice")
    amount_total_to_pay = fields.Monetary(string='Tổng phải trả', store=True, compute='_compute_amount_total_to_pay')
    amount_total = fields.Monetary(string='Tổng hóa đơn', store=True, readonly=True, compute='_compute_invoice')
    count_invoice_ids = fields.Integer()
    time_for_Payment = fields.Datetime(string="Thời hạn thanh toán", default=fields.Datetime.now)
    mode_of_payment = fields.Selection([('cash', 'Tiền mặt'),
                                        ('transfer', 'Chuyển khoản')], string="Phương thức thanh toán", default='cash')
    bank_ids = fields.Many2one('res.partner.bank', string='Ngân hàng')
    bank_acc_holder = fields.Text('Chủ tài khoản', store=True)
    bank_acc_number = fields.Char('Số Tài khoản', store=True)
    bank_acc_holder_address = fields.Char('Địa chỉ tài khoản', store=True)
    bank_name = fields.Char('Tên ngân hàng', readonly=False)
    bank_address = fields.Char('Địa chỉ ngân hàng', store=True)

    @api.multi
    @api.onchange('bank_ids')
    def _compute_bank(self):
        bank_acc_holder = self.bank_ids.partner_id
        self.bank_acc_number = self.bank_ids.acc_number
        self.bank_name = self.bank_ids.bank_name
        acc_address = ', '
        if bank_acc_holder:
            if bank_acc_holder.street:
                acc_address += str(bank_acc_holder.street)
            if bank_acc_holder.state_id:
                acc_address += ', ' + str(bank_acc_holder.state_id.name)
            if bank_acc_holder.country_id:
                acc_address += ', ' + str(bank_acc_holder.country_id.name)
            if len(acc_address) >= 2:
                acc_address = acc_address[2:]
            self.bank_acc_holder_address = acc_address
            self.bank_acc_holder = bank_acc_holder.name
        bank_address = ', '
        bank = self.bank_ids.bank_id
        if bank:
            if bank.street:
                bank_address += str(bank.street)
            if bank.state:
                bank_address += ', ' + str(bank.state_id.name)
            if bank.country:
                bank_address += ', ' + str(bank.country_id.name)
            if len(bank_address) >= 2:
                bank_address = bank_address[2:]
            self.bank_address = bank_address

    @api.onchange('purchase_id')
    def _onchange_purchase_id(self):
        domain = {}
        if self.purchase_id:
            domain = {'bank_ids': [('partner_id', '=', self.purchase_id.partner_id.id)]}
        return {'domain': domain}

    @api.one
    @api.depends('purchase_id')
    def _compute_invoice(self):
        for p in self:
            invoice_ids = []
            invoice_ids_paid = []
            for i in p.purchase_id.invoice_ids:
                if i.state == 'open':
                    invoice_ids.append(i.id)
                elif i.state == 'paid' or i.state == 'in_payment':
                    invoice_ids_paid.append(i.id)
            p.invoice_ids_paid = invoice_ids_paid
            size = len(invoice_ids)
            if size > 0:
                p.invoice_ids = invoice_ids
            p.count_invoice_ids = size
            p.currency_id = p.purchase_id.currency_id
            p.amount_total = p.purchase_id.amount_total
            p.bank_ids = None

    @api.one
    @api.depends('invoice_ids.residual_signed')
    def _compute_amount_total_to_pay(self):
        for p in self:
            amount_total_to_pay = 0
            for i in p.invoice_ids:
                if i.state == 'open':
                    amount_total_to_pay += i.residual_signed
            self.amount_total_to_pay = amount_total_to_pay

    def get_bill_numbers(self):
        s = ""
        for b in self.invoice_ids:
            s += "; " + b.number

        lenght = len(s)
        if lenght > 0:
            return s[1:]
        return s

    @api.model
    def readNum(self, num):
        return readFreeNum(int(num))

    @api.multi
    def print(self):
        datas = {'ids': self._ids,
                 'form': self.read()[0],
                 'model': 'purchase.payment.request'
                 }
        # print(self.purchase_id.company_id)
        return self.env.ref('sc_purchase_payment_request.report_payment_request_purchase_pdf').report_action(self)

    @api.model
    def get_time_of_payment(self):
        if self.time_for_Payment:
            return self.time_for_Payment.strftime("%d/%m/%Y")
        return ""

    @api.model
    def format_date(self, date):
        if date:
            return date.strftime("%d/%m/%Y")
        return ""
