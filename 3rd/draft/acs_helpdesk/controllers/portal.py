# -*- coding: utf-8 -*-
from collections import OrderedDict

from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
from odoo.http import request
import base64


class HelpdeskPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(HelpdeskPortal, self)._prepare_portal_layout_values()
        user = request.env.user
        ticket_count = request.env['acs.support.ticket'].sudo().search_count([('partner_id', '=', user.partner_id.id)])
        values.update({
            'ticket_count': ticket_count,
        })
        return values

    @http.route(['/my/tickets', '/my/tickets/page/<int:page>'], type='http', auth="user", website=True)
    def my_tickets(self, page=1, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        user = request.env.user
        if not sortby:
            sortby = 'date'

        sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
        }

        order = sortings.get(sortby, sortings['date'])['order']
 
        pager = portal_pager(
            url="/my/tickets",
            url_args={},
            total=values['ticket_count'],
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        tickets = request.env['acs.support.ticket'].sudo().search([
                ('partner_id', '=', user.partner_id.id)], 
                order=order, limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'sortings': sortings,
            'sortby': sortby,
            'tickets': tickets,
            'page_name': 'ticket',
            'default_url': '/my/tickets',
            'searchbar_sortings': sortings,
            'pager': pager
        })
        return request.render("acs_helpdesk.my_tickets", values)

    @http.route(['/my/tickets/<int:ticket_id>'], type='http', auth="user", website=True)
    def my_tickets_ticket(self, ticket_id=None, **kw):
        ticket = request.env['acs.support.ticket'].browse(ticket_id)
        return request.render("acs_helpdesk.my_tickets_ticket", {'ticket': ticket})

    @http.route('/support/help', type="http", auth="user", website=True)
    def support_create_ticket(self, **kw):
        data = {
            'categories': request.env['acs.support.ticket.categories'].sudo().search([]), 
            'email': request.env.user.email
        }
        return request.render('acs_helpdesk.support_create_ticket', data)

    @http.route('/support/ticket/create', type="http", auth="user", website=True, csrf=True)
    def support_submit_ticket(self, **kwargs):
        new_ticket_id = request.env['acs.support.ticket'].sudo().create({
            'category_id': kwargs.get('category',False), 
            'email': kwargs['email'], 
            'description': kwargs['description'],
            'name': kwargs['name'], 
            'partner_id': http.request.env.user.partner_id.id, 
        })

        if 'file' in kwargs:
            for c_file in request.httprequest.files.getlist('file'):
                data = c_file.read()

                if c_file.filename:
                    request.env['ir.attachment'].sudo().create({
                        'name': c_file.filename,
                        'datas': base64.b64encode(data),
                        'datas_fname': c_file.filename,
                        'res_model': 'acs.support.ticket',
                        'res_id': new_ticket_id.id
                    })

        return request.render("acs_helpdesk.support_thank_you", {'ticket': new_ticket_id})
