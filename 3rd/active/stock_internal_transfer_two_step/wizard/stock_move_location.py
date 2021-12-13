# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.fields import first


class StockMoveLocationWizard(models.TransientModel):
    _name = "wiz.stock.move.location"
    _description = 'Wizard move location'

    origin_location_id = fields.Many2one(string='Origin Location', comodel_name='stock.location', required=True)
    destination_location_id = fields.Many2one(string='Destination Location', comodel_name='stock.location', required=False)
    stock_move_location_line_ids = fields.One2many('wiz.stock.move.location.line', 'wizart_id', string="Move Location lines")
    picking_id = fields.Many2one(string="Connected Picking", comodel_name="stock.picking")
    product_ids = fields.Many2many(comodel_name="product.product", relation='tgl_move_location_product_rel', column1='product_id', column2='wiz_id', string="Products")

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        stock_piking = self.env['stock.picking'].browse(
            self.env.context.get('active_ids'))
        lines = stock_piking.internal_move_ids
        if (self._context.get('is_receipt')):
            res['origin_location_id'] = stock_piking.picking_type_id.warehouse_id.internal_transfer_location_id.id
            res['destination_location_id'] = stock_piking.location_dest_id.id
            enable_split = stock_piking.picking_type_id.warehouse_id.internal_transfer_location_id.get_warehouse().enable_auto_split
        else:
            res['origin_location_id'] = stock_piking.location_id.id
            res['destination_location_id'] = stock_piking.picking_type_id.warehouse_id.internal_transfer_location_id.id
            enable_split = stock_piking.location_id.get_warehouse().enable_auto_split

        res['picking_id'] = stock_piking.id
        res['product_ids'] = [(6, 0, lines.mapped('product_id').ids)]
        res['stock_move_location_line_ids'] = []

        if not enable_split:
            return res
        for line in lines:
            search_args = [
                ('location_id', '=', res['origin_location_id']),
                ('product_id', '=', line.product_id.id),
            ]
            quants = self.env['stock.quant'].read_group(search_args, ['product_id', 'lot_id', 'quantity'], ['lot_id'])
            if (quants):
                count_quant = 0
                for quant in quants:
                    if ((count_quant + quant['quantity']) <= line.max_quantity):
                        count_quant = count_quant + quant['quantity']
                    else:
                        quantity_set = line.max_quantity - count_quant
                        res['stock_move_location_line_ids'].append(((0, 0, {
                            'product_id': line.product_id.id,
                            'move_quantity': quantity_set,
                            'max_quantity': quant['quantity'],
                            'origin_location_id': res['origin_location_id'],
                            'destination_location_id': res['destination_location_id'],
                            'lot_id': quant['lot_id'][0],
                            'product_uom_id': line.product_id.uom_id.id,
                            'custom': False,
                        })))
                        break

                    res['stock_move_location_line_ids'].append(((0, 0, {
                        'product_id': line.product_id.id,
                        'move_quantity': quant['quantity'],
                        'max_quantity': quant['quantity'],
                        'origin_location_id': res['origin_location_id'],
                        'destination_location_id': res['destination_location_id'],
                        'lot_id': quant['lot_id'][0],
                        'product_uom_id': line.product_id.uom_id.id,
                        'custom': False,
                    })))
            else:
                res['stock_move_location_line_ids'].append(((0, 0, {
                        'product_id': line.product_id.id,
                        'move_quantity': 0,
                        'max_quantity': line.max_quantity,
                        'origin_location_id': res['origin_location_id'],
                        'destination_location_id': res['destination_location_id'],
                        'lot_id': line.lot_id.id,
                        'product_uom_id': line.product_id.uom_id.id,
                        'custom': False,
                    })))

        return res

    def _clear_lines(self):
        self.stock_move_location_line_ids = False

    def _get_locations_domain(self):
        return [('usage', '=', 'internal')]

    def _create_picking(self):
        return self.env['stock.picking'].create({
            'picking_type_id': self.env.ref('stock.picking_type_internal').id,
            'location_id': self.origin_location_id.id,
            'location_dest_id': self.destination_location_id.id,
        })

    def group_lines(self):
        lines_grouped = {}
        for line in self.stock_move_location_line_ids:
            lines_grouped.setdefault(
                line.product_id.id,
                self.env["wiz.stock.move.location.line"].browse(),
            )
            lines_grouped[line.product_id.id] |= line
        return lines_grouped

    def _create_moves(self, picking):
        self.ensure_one()
        groups = self.group_lines()
        moves = self.env["stock.move"]
        for lines in groups.values():
            move = self._create_move(picking, lines)
            moves |= move
        return moves

    def _get_move_values(self, picking, lines):
        # locations are same for the products
        location_from_id = lines[0].origin_location_id.id
        location_to_id = lines[0].destination_location_id.id
        product = lines[0].product_id
        product_uom_id = lines[0].product_uom_id.id
        qty = sum([x.move_quantity for x in lines])
        return {
            "name": product.display_name,
            "location_id": location_from_id,
            "location_dest_id": location_to_id,
            "product_id": product.id,
            "product_uom": product_uom_id,
            "product_uom_qty": qty,
            "picking_id": picking.id,
            # "location_move": True,
        }

    def _create_move(self, picking, lines):
        self.ensure_one()
        move = self.env["stock.move"].create(
            self._get_move_values(picking, lines),
        )
        for line in lines:
            line.create_move_lines(picking, move)
        return move

    def action_move_location(self):
        self.ensure_one()
        picking = self.picking_id
        self._create_moves(picking)
        if not self.env.context.get("planned"):
            picking.button_validate()
        msg = _('<div>From <b>{}</b> to <b>{}</b></div>'.format(self.origin_location_id.display_name, self.destination_location_id.display_name))
        msg_line = '''<tr>
            <td>{}{}</td>
            <td>{}</td>
            <td>{}</td>
        </tr>'''
        msg_content = '''
            <table class="table table-bordered">
                <thead><tr><th>Product</th><th>Lot</th><th>Quantity</th></tr></thead>
                <tbody>{}</tbody>
            </table>
        '''
        msg_table = ''
        for line in self.stock_move_location_line_ids:
            location_name = ''
            if self.origin_location_id != line.origin_location_id or self.destination_location_id != line.destination_location_id:
                location_name = ': {} to {}'.format(line.origin_location_id.display_name, line.destination_location_id.display_name)
            msg_table += msg_line.format(line.product_id.name, location_name, line.lot_id and line.lot_id.display_name or '', line.move_quantity)
        picking.message_post(body=msg + msg_content.format(msg_table))
        picking.tgl_update_state()

    def _get_picking_action(self, pickinig_id):
        action = self.env.ref("stock.action_picking_tree_all").read()[0]
        form_view = self.env.ref("stock.view_picking_form").id
        action.update({
            "view_mode": "form",
            "views": [(form_view, "form")],
            "res_id": pickinig_id,
        })
        return action

    def _get_group_quants(self):
        location_id = self.origin_location_id.id
        company = self.env['res.company']._company_default_get(
            'stock.inventory',
        )
        # Using sql as search_group doesn't support aggregation functions
        # leading to overhead in queries to DB
        query = """
            SELECT product_id, lot_id, SUM(quantity)
            FROM stock_quant
            WHERE location_id = %s
            AND company_id = %s
            GROUP BY product_id, lot_id
        """
        self.env.cr.execute(query, (location_id, company.id))
        return self.env.cr.dictfetchall()

    def _get_stock_move_location_lines_values(self):
        product_obj = self.env['product.product']
        product_data = []
        for group in self._get_group_quants():
            product = product_obj.browse(group.get("product_id")).exists()
            product_data.append({
                'product_id': product.id,
                'move_quantity': group.get("sum"),
                'max_quantity': group.get("sum"),
                'origin_location_id': self.origin_location_id.id,
                'destination_location_id': self.destination_location_id.id,
                # cursor returns None instead of False
                'lot_id': group.get("lot_id") or False,
                'product_uom_id': product.uom_id.id,
                'custom': False,
            })
        return product_data

    def clear_lines(self):
        self._clear_lines()
        return {
            "type": "ir.action.do_nothing",
        }
