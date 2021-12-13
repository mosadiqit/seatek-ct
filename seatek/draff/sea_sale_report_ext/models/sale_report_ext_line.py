# -*- coding: utf-8 -*-
import odoo.addons.decimal_precision as dp
import base64, json, pydot
from odoo import fields, models, tools, api
from odoo.exceptions import ValidationError
from psycopg2.extensions import AsIs


class SeaExtSaleOrderLineReport(models.Model):
    _name = 'sea_sale_report_ext.report_line'
    _description = 'Sale Report Extension line'
    _auto = False

    # report_id = fields.Many2one('sea_sale_report_ext.report', ondelete='cascade')
    order_id = fields.Many2one('sale.order',string='Order', readonly=True, store=True)
    product_id = fields.Many2one('product.product',string='Product', readonly=True, store=True)
    name = fields.Char(string='Description', readonly=True, store=True)
    product_uom = fields.Many2one('uom.uom',string='UoM', readonly=True, store=True)
    price_unit = fields.Float(string='Unit Price', digits=dp.get_precision('Product Price'), default=0.0, readonly=True, store=True)
    product_uom_qty = fields.Float(string='Ordered Quantity', digits=dp.get_precision('Product Unit of Measure'), readonly=True, store=True)
    qty_pick_int = fields.Float(string='PickInt Qty', readonly=True, store=True)
    qty_delivered = fields.Float('Delivered Quantity', copy=False,  inverse='_inverse_qty_delivered', compute_sudo=True, digits=dp.get_precision('Product Unit of Measure'), default=0.0, readonly=True, store=True)
    qty_invoiced = fields.Float(
        string='Invoiced Quantity', readonly=True, store=True,
        digits=dp.get_precision('Product Unit of Measure'))
    discount = fields.Float(string='Discount (%)',  digits=dp.get_precision('Discount'), default=0.0, readonly=True, store=True)
    price_reduce = fields.Float( string='Price Reduce', digits=dp.get_precision('Product Price'), readonly=True, store=True)
    price_tax = fields.Float( string='Total Tax', readonly=True, store=True)
    # price_total = fields.Monetary( string='Total', readonly=True, store=True)
    state = fields.Selection([('draft', 'Quotation'), ('sent', 'Quotation Sent'), ('sale', 'Sales Order'), ('done', 'Locked'), ('cancel', 'Cancelled')], string='Order Status', readonly=True, store=True)
    invoice_status = fields.Selection([
                        ('upselling', 'Upselling Opportunity'),
                        ('invoiced', 'Fully Invoiced'),
                        ('to invoice', 'To Invoice'),
                        ('no', 'Nothing to Invoice')
                        ], string='Invoice Status', readonly=True, store=True, default='no')
    salesman_id = fields.Many2one(related='order_id.user_id', string='Salesperson', readonly=True, store=True)
    order_partner_id = fields.Many2one(related='order_id.partner_id', string='Customer', readonly=True, store=True)
    tab_query = """
SELECT
    CAST ( ROW_NUMBER () OVER () AS INTEGER ) AS "id",
        report.order_id AS order_id,
        report.product_id AS product_id,
        report."name" AS "name",
        report.product_uom AS product_uom,
        report.price_unit AS price_unit,
        report.product_uom_qty AS product_uom_qty,
        Sum(move_stock.product_qty) AS qty_pick_int,
        report.qty_delivered AS qty_delivered,
        report.qty_invoiced AS qty_invoiced,
        report.discount AS discount,
        report.price_reduce AS price_reduce,
        report.price_tax AS price_tax,
        report."state" AS "state",
        report.invoice_status AS invoice_status,
        report.salesman_id AS salesman_id,
        report.order_partner_id AS order_partner_id

    FROM
        "public".sale_order_line AS report
        INNER JOIN "public".stock_move AS move_stock ON move_stock.sale_line_id = report."id"
        INNER JOIN "public".stock_picking AS picking ON picking.sale_id = report.order_id
        INNER JOIN "public".sale_order AS sale_order ON report.order_id = sale_order."id" AND picking.sale_id = sale_order."id" AND sale_order.warehouse_id = move_stock.warehouse_id

    WHERE
        report."id" = move_stock.sale_line_id AND
        picking."id" = move_stock.picking_id
    GROUP BY
        report."id",
        report.order_id,
        report.product_id,
        report."name",
        report.product_uom,
        report.price_unit,
        report.product_uom_qty,
        report.qty_delivered,
        report.qty_invoiced,
        report.discount,
        report.price_reduce,
        report.price_tax,
        report."state",
        report.invoice_status,
        report.salesman_id,
        report.order_partner_id
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