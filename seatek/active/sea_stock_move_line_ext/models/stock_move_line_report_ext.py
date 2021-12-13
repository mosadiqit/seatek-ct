# -*- coding: utf-8 -*-
import odoo.addons.decimal_precision as dp
import base64, json, pydot
from odoo import fields, models, tools, api
from odoo.exceptions import ValidationError
from psycopg2.extensions import AsIs


class SeaExtSaleOrderLineReport(models.Model):
    _name = 'sea_stock_move_line_ext.report_line'
    _description = 'Stock Move Line Report Extension'
    _auto = False

    date = fields.Datetime('Date', default=fields.Datetime.now, readonly=True, store=True)
    reference = fields.Char(string='Sequence', readonly=True, store=True)
    product_id = fields.Many2one('product.product', 'Product', ondelete="cascade", readonly=True, store=True)
    location_id = fields.Many2one('stock.location', 'From', readonly=True, store=True)
    location_dest_id = fields.Many2one('stock.location', 'To', readonly=True, store=True)
    qty_done = fields.Float('Done', default=0.0, digits=dp.get_precision('Product Unit of Measure'), readonly=True, store=True)
    product_uom_id = fields.Many2one('uom.uom', 'Unit of Measure', readonly=True, store=True)
    state = fields.Selection([
        ('draft', 'New'), ('cancel', 'Cancelled'),
        ('waiting', 'Waiting Another Move'),
        ('confirmed', 'Waiting Availability'),
        ('partially_available', 'Partially Available'),
        ('assigned', 'Available'),
        ('done', 'Done')], string='Status',readonly=True, store=True,)
    partner_id = fields.Many2one(
        'res.partner', 'Partner',
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}, readonly=True, store=True)
    origin = fields.Char(
        'Source Document', index=True,
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
        help="Reference of the document", readonly=True, store=True)
    tab_query = """
SELECT
    CAST ( ROW_NUMBER () OVER () AS INTEGER ) AS "id",
        report."date" AS "date",
        report.reference AS reference,
        report.product_id AS product_id,
        report.location_id AS location_id,
        report.location_dest_id AS location_dest_id,
        report.qty_done AS qty_done,
        report.product_uom_id AS product_uom_id,
        report."state" AS "state",
        picking.partner_id AS partner_id,
        picking.origin AS origin
    FROM
        "public".stock_move_line AS report
        INNER JOIN "public".stock_picking AS picking ON report.picking_id = picking."id"
        """

    @api.model_cr
    def init(self):
        table = self._table
        query = self.tab_query and self.tab_query.replace('\n', ' ')
        # self._cr.execute('DROP TABLE IF EXISTS %s', (AsIs(table),))
        self.env.cr.execute('CREATE or REPLACE VIEW %s as (%s)', (AsIs(table), AsIs(query),))

    def report_update(self):
        table = self._table
        query = self.tab_query and self.tab_query.replace('\n', ' ')
        # self._cr.execute('DROP TABLE IF EXISTS %s', (AsIs(table),))
        res_all = self.env.cr.execute('CREATE or REPLACE VIEW %s as (%s)', (AsIs(table), AsIs(query), ))
        # res_all = self._cr.fetchall()
        return res_all