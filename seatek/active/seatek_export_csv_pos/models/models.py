# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json


class SeatekPOSOrder(models.Model):
    _inherit = ['pos.order']

    @api.multi
    def export_csv(self):
        print(self.number)

        filename = self.number.replace("/", "-")

        data = {'model': self._name,
                'fields': [{'name': 'id', 'label': 'ID'},
                           {'name': 'name', 'label': 'Order Ref'},
                           {'name': 'pos_reference', 'label': 'Receipt Ref'},
                           {'name': 'partner_id/id', 'label': 'Customer/ID'},
                           {'name': 'partner_id/name', 'label': 'Customer/name'},
                           {'name': 'date_order', 'label': 'Order Date'},
                           {'name': 'user_id/name', 'label': 'Salesperson/Name'},
                           {'name': 'amount_total', 'label': 'Total'},
                           {'name': 'company_id/name', 'label': 'Company'},
                           {'name': 'state', 'label': 'Status'},
                           {'name': 'session_id/name', 'label': 'Session'}],
                'ids': [self.id]}
        #,'domain': [["type", "=", "out_invoice"]], 'context': self._context, 'import_compat': False
        j = json.dumps(data)
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/export/csv?data=%s&token=%s' % (j, ""),
            'target': 'new',
        }

        # filecontent = "aaaaaa"
        # if not filecontent:
        #     return request.not_found()
        # else:
        #     if not filename:
        #         filename = '%s_%s' % (model.replace('.', '_'), id)
        #         return request.make_response(filecontent,
        #                                      [('Content-Type', 'application/octet-stream'),
        #                                       ('Content-Disposition', content_disposition(filename))])
