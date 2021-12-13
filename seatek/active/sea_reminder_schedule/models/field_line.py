#coding: utf-8

from odoo import api, fields, models


class field_line(models.Model):
    _name = "sea_reminder_schedule_fields.line"
    _description = 'Field Line'

    @api.multi
    @api.depends("field_id")
    def _compute_model_from_field_id(self):
        """
        Compute method for model_from_field_id

        Attrs update:
         * model_from_field_id - as model of linked field if exist
        """
        for line in self:
            model_from_field_id = False
            field = line.field_id
            if field and field.ttype in ["many2one", "one2many", "many2many"]:
                model_from_field_id = self.env['ir.model'].search(
                    [('model', '=', field.relation)],
                    limit=1,
                )
            line.model_from_field_id = model_from_field_id

    @api.multi
    @api.onchange('field_id', 'related_field')
    def onchange_field_id(self):
        """
        Onchange method for field_id and related_field
        The goal is to take translated version of field (field_description doesn't have own)

        Methods:
         * _return_translation_for_field_label of sea_reminder_schedule.mail
        """
        for line in self:
            field = line.related_field or line.field_id or False
            if field:
                line.field_label = line.sea_reminder_schedule_id._return_translation_for_field_label(
                    field=field)

    sequence = fields.Integer(string='Sequence')
    sea_reminder_schedule_id = fields.Many2one(
        'sea_reminder_schedule.mail',
        string='Notification',
    )
    field_id = fields.Many2one(
        'ir.model.fields',
        string='Column',
        required=True,
    )
    field_label = fields.Char(string='Label', required=True)
    model_from_field_id = fields.Many2one("ir.model",
                                          string="Model",
                                          compute=_compute_model_from_field_id,
                                          store=True,
                                          help="""
            Technical field to restrict selection of fields related only to this many2one model
        """)
    related_field = fields.Many2one(
        'ir.model.fields',
        string=u"Complementary",
        required=False,
    )

    _order = "sequence, id"
