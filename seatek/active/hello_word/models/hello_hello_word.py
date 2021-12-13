from odoo import fields, models

class HelloWord(models.Model):
    _name = 'table.hello'
    _description = 'Hello Word'

    name = fields.Char(string="Name")
    img = fields.Binary(string="Image")
    fields2 = fields.Integer("Fields2")
    fields3 = fields.Text(string="Fields3", required=True)
    fields4 = fields.Char(string="Fields4", required=True)
    fields5 = fields.Text(string="Fields5")
