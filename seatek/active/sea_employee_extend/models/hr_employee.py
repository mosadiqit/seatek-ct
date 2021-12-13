# -*- coding: utf-8 -*-
###################################################################################
#    A part of Open HRMS Project <https://www.openhrms.com>
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2018-TODAY Cybrosys Technologies (<https://www.cybrosys.com>).
#    Author: Jesni Banu (<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################
from datetime import datetime, timedelta
from odoo import models, fields, _

GENDER_SELECTION = [('male', 'Male'),
                    ('female', 'Female'),
                    ('other', 'Other')]


class HrEmployeeContactName(models.Model):
    """This class is to add emergency contact table"""

    _name = 'hr.emergency.contact'
    _description = 'HR Emergency Contact'

    number = fields.Char(string='Number', help='Contact Number')
    relation = fields.Char(string='Contact', help='Relation with employee')
    employee_obj = fields.Many2one('hr.employee', invisible=1)


class HrEmployeeFamilyInfo(models.Model):
    """Table for keep employee family information"""

    _name = 'hr.employee.family'
    _description = 'HR Employee Family'

    employee_id = fields.Many2one('hr.employee', string="Employee", help='Select corresponding Employee',
                                  invisible=1)

    member_name = fields.Char(string='Name')
    relation = fields.Selection([('father', 'Father'),
                                 ('mother', 'Mother'),
                                 ('wife', 'Wife'),
								 ('husband', 'Husband'),
                                 ('child', 'Child'),
                                 ('brother', 'Brother'),
                                 ('sister', 'Sister'),
                                 ('relative', 'Relative'),
                                 ('others', 'Others')], string='Relationship', help='Relation with employee')
    member_contact = fields.Char(string='Contact No')
    emergency = fields.Selection([('Y', 'Yes'),
                                 ('N', 'No')], string='Emergency', help='Emergency Contact')
    member_independent = fields.Selection([('Y', 'Yes'),
                                 ('N', 'No')], string='Independent', help='Member Income Independent')
    member_gender = fields.Selection([('M', 'Male'),
                                 ('F', 'Female')], string='Gender', help='Member Gender')
    member_address = fields.Char(string='Address')
    member_birthday = fields.Date(string='Birthday')
    member_phone = fields.Char(string='Phone')
    member_taxcode = fields.Char(string='Tax Code')
    member_note = fields.Char(string='Note')

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def mail_reminder(self):
        """Sending expiry date notification for ID and Passport"""

        now = datetime.now() + timedelta(days=1)
        date_now = now.date()
        match = self.search([])
        for i in match:
            if i.id_expiry_date:
                exp_date = fields.Date.from_string(i.id_expiry_date) - timedelta(days=14)
                if date_now >= exp_date:
                    mail_content = "  Hello  " + i.name + ",<br>Your ID " + i.identification_id + "is going to expire on " + \
                                   str(i.id_expiry_date) + ". Please renew it before expiry date"
                    main_content = {
                        'subject': _('ID-%s Expired On %s') % (i.identification_id, i.id_expiry_date),
                        'author_id': self.env.user.partner_id.id,
                        'body_html': mail_content,
                        'email_to': i.work_email,
                    }
                    self.env['mail.mail'].sudo().create(main_content).send()
        match1 = self.search([])
        for i in match1:
            if i.passport_expiry_date:
                exp_date1 = fields.Date.from_string(i.passport_expiry_date) - timedelta(days=180)
                if date_now >= exp_date1:
                    mail_content = "  Hello  " + i.name + ",<br>Your Passport " + i.passport_id + "is going to expire on " + \
                                   str(i.passport_expiry_date) + ". Please renew it before expiry date"
                    main_content = {
                        'subject': _('Passport-%s Expired On %s') % (i.passport_id, i.passport_expiry_date),
                        'author_id': self.env.user.partner_id.id,
                        'body_html': mail_content,
                        'email_to': i.work_email,
                    }
                    self.env['mail.mail'].sudo().create(main_content).send()
    personal_mobile = fields.Char(string='Mobile', related='address_home_id.mobile', store=True)
    joining_date = fields.Date(string='Joining Date')
    ''' htkhoa + '''
    sea_id_issue_date = fields.Date(string='ID Issue Date', help='Issue date of Identification ID')
    sea_id_issue_place = fields.Char(string='ID Issue Place', help='Issue Place Identification ID')

    id_expiry_date = fields.Date(string='ID Expiry Date', help='Expiry date of Identification ID')
    ''' htkhoa + '''
    sea_passport_issue_date = fields.Date(string='Passport Issue Date', help='Issue date of Passport')
    sea_passport_issue_place = fields.Char(string='Passport Issue Place', help='Issue Place Passport')
    ''' htkhoa - '''

    passport_expiry_date = fields.Date(string='Passport Expiry Date', help='Expiry date of Passport ID')
    id_attachment_id = fields.Many2many('ir.attachment', 'id_attachment_rel', 'id_ref', 'attach_ref',
                                        string="Attachment", help='You can attach the copy of your Id')
    passport_attachment_id = fields.Many2many('ir.attachment', 'passport_attachment_rel', 'passport_ref', 'attach_ref1',
                                              string="Attachment",
                                              help='You can attach the copy of Passport')
    fam_ids = fields.One2many('hr.employee.family', 'employee_id', string='Family', help='Family Information')
    emergency_contacts = fields.One2many('hr.emergency.contact', 'employee_obj', string='Emergency Contact')

    ''' htkhoa add '''
    sea_permanent_addr = fields.Char(string='Permanent Address')
    sea_temp_addr = fields.Char(string='Temporary Address')
    sea_personal_email = fields.Char(string='Personal Email')
