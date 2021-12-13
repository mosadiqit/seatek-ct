# -*- coding: utf-8 -*-
from odoo import http

# class SeatekExportCsvPos(http.Controller):
#     @http.route('/seatek_export_csv_pos/seatek_export_csv_pos/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/seatek_export_csv_pos/seatek_export_csv_pos/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('seatek_export_csv_pos.listing', {
#             'root': '/seatek_export_csv_pos/seatek_export_csv_pos',
#             'objects': http.request.env['seatek_export_csv_pos.seatek_export_csv_pos'].search([]),
#         })

#     @http.route('/seatek_export_csv_pos/seatek_export_csv_pos/objects/<model("seatek_export_csv_pos.seatek_export_csv_pos"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('seatek_export_csv_pos.object', {
#             'object': obj
#         })