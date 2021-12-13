# -*- coding: utf-8 -*-
from odoo import http

# class SeatekMrp(http.Controller):
#     @http.route('/seatek_mrp/seatek_mrp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/seatek_mrp/seatek_mrp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('seatek_mrp.listing', {
#             'root': '/seatek_mrp/seatek_mrp',
#             'objects': http.request.env['seatek_mrp.seatek_mrp'].search([]),
#         })

#     @http.route('/seatek_mrp/seatek_mrp/objects/<model("seatek_mrp.seatek_mrp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('seatek_mrp.object', {
#             'object': obj
#         })