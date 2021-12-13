# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError
from ast import literal_eval


class InternalStockMove(models.Model):
    _name = 'internal.stock.move'
    _description = 'Internal stock move'

    picking_id = fields.Many2one('stock.picking', 'Internal transfer')
    product_id = fields.Many2one('product.product', 'Product', required=True)
    location_id = fields.Many2one('stock.location', 'Origin Location', )
    location_dest_id = fields.Many2one('stock.location', 'Destination Location')
    product_uom_id = fields.Many2one('uom.uom', 'Product Unit of Measure')
    lot_id = fields.Many2one('stock.production.lot', 'Lot/Serial Number', domain="[('product_id','=',product_id)]")
    move_quantity = fields.Float('Quantity to move', digits=dp.get_precision('Product Unit of Measure'),)
    move_send_done = fields.Float('Sended', digits=dp.get_precision('Product Unit of Measure'), readonly=True)
    move_receipt_done = fields.Float('Receipted', digits=dp.get_precision('Product Unit of Measure'), readonly=True)
    max_quantity = fields.Float('Initial demand', digits=dp.get_precision('Product Unit of Measure'),)
    custom = fields.Boolean('Custom line', default=True)

    @api.constrains('move_send_done', 'move_receipt_done')
    def check_move_qualiti(self):
        if self.move_quantity > self.max_quantity - self.move_send_done:
            raise ValidationError(_("The quantity can't over the initial demand!"))
        if self.move_quantity > self.max_quantity - self.move_receipt_done:
            raise ValidationError(_("The quantity can't over the initial demand!"))
        if self.move_quantity + self.move_receipt_done > self.move_send_done:
            raise ValidationError(_("The quantity can't over the quantity in transit location!"))

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.onchange('tgl_vitual_location_id')
    def _onchange_tgl_vitual_location_id(self):
        if self.tgl_vitual_location_id:
            self.location_id = self.tgl_vitual_location_id

    @api.onchange('location_id')
    def _onchange_tgl_location_id(self):
        if self.location_id and self.location_id != self.tgl_vitual_location_id:
            self.tgl_vitual_location_id = self.location_id

    @api.onchange('tgl_vitual_location_dest_id')
    def _onchange_tgl_vitual_location_dest_id(self):
        if self.tgl_vitual_location_dest_id:
            self.location_dest_id = self.tgl_vitual_location_dest_id

    @api.onchange('location_dest_id')
    def _onchange_tgl_location_dest_id(self):
        if self.location_dest_id and self.location_dest_id != self.tgl_vitual_location_dest_id:
            self.tgl_vitual_location_dest_id = self.location_dest_id

    @api.depends('picking_type_code', 'location_id', 'location_dest_id')
    def _tgl_compute_apply_two_step_auth(self):
        for picking in self:
            picking.apply_two_step_auth = picking.picking_type_code == 'internal' and picking.location_id.get_warehouse() != picking.location_dest_id.get_warehouse()

    internal_transfer_state = fields.Selection([
        ('draft', 'Draft'),
        ('partial_send', 'Partial send'),
        ('sended', 'Sended'),
        ('partial_receipt', 'Partial receipt'),
        ('done', 'Done'),
        ('cancel', 'Cancel')],
        string='Internal transfer state', default='draft')

    state = fields.Selection(selection_add=[('partial_send', 'Partial send'), ('sended', 'Sended'), ('partial_receipt', 'Partial receipt')])

    internal_move_ids = fields.One2many('internal.stock.move', 'picking_id', 'Internal moves')

    tgl_vitual_location_id = fields.Many2one('stock.location', 'Source Location', domain=[('usage', '=', 'internal')], readonly=True, states={'draft': [('readonly', False)]})
    tgl_vitual_location_dest_id = fields.Many2one('stock.location', 'Destination Location', domain=[('usage', '=', 'internal')], readonly=True, states={'draft': [('readonly', False)]})

    apply_two_step_auth = fields.Boolean('Apply internal authencation with two step', compute='_tgl_compute_apply_two_step_auth', compute_sudo=True, store=True)

    @api.depends('move_type', 'move_lines.state', 'move_lines.picking_id', 'picking_type_code', 'internal_transfer_state', 'apply_two_step_auth')
    def _compute_state(self):
        internal_transfer = self.filtered(lambda r: r.apply_two_step_auth)
        for record in internal_transfer:
            record.state = record.internal_transfer_state
        super(StockPicking, self - internal_transfer)._compute_state()

    def tgl_send(self):
        user_permiss_ids = self.location_id.get_warehouse().user_permis_ids
        if not self.env.user.id in user_permiss_ids.ids:
            raise ValidationError(_("You can not excute this action, please contact with administritor!"))
        return self.env.ref('stock_internal_transfer_two_step.wiz_stock_move_location_action').read()[0]

    def tgl_cancel(self):
        self.internal_transfer_state = 'cancel'

    def tgl_receipt(self):
        user_permiss_ids = self.location_dest_id.get_warehouse().user_permis_ids
        if not self.env.user.id in user_permiss_ids.ids:
            raise ValidationError(_("You can not excute this action, please contact with administritor!"))
        return self.env.ref('stock_internal_transfer_two_step.wiz_stock_move_location_action').read()[0]

    def tgl_update_state(self):
        if all(line.move_send_done == line.max_quantity for line in self.internal_move_ids) and all(line.move_receipt_done == line.max_quantity for line in self.internal_move_ids):
            self.internal_transfer_state = 'done'
        elif all(line.move_send_done == line.max_quantity for line in self.internal_move_ids):
            if any(line.move_receipt_done > 0 for line in self.internal_move_ids):
                self.internal_transfer_state = 'partial_receipt'
            else:
                self.internal_transfer_state = 'sended'
        elif any(line.move_send_done > 0 for line in self.internal_move_ids):
            self.internal_transfer_state = 'partial_send'

class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    count_picking_partial_send = fields.Integer(compute='_compute_picking_count')
    count_picking_sended = fields.Integer(compute='_compute_picking_count')
    count_picking_partial_receipt = fields.Integer(compute='_compute_picking_count')

    def _compute_picking_count(self):
        super(StockPickingType, self)._compute_picking_count()
        internal_transfer = self.filtered(lambda r: r.code == 'internal')
        PickingObj = self.env['stock.picking']
        for record in internal_transfer:
            record.count_picking_ready = PickingObj.search_count([('state', 'in', ('assigned', 'partial_send', 'sended', 'partial_receipt')), ('picking_type_id', '=', record.id)])
            record.count_picking_partial_send = PickingObj.search_count([('state', '=', 'partial_send'), ('picking_type_id', '=', record.id)])
            record.count_picking_sended = PickingObj.search_count([('state', '=', 'sended'), ('picking_type_id', '=', record.id)])
            record.count_picking_partial_receipt = PickingObj.search_count([('state', '=', 'partial_receipt'), ('picking_type_id', '=', record.id)])
        for record in (self - internal_transfer):
            record.count_picking_sended = 0
            record.count_picking_partial_send = 0
            record.count_picking_partial_receipt = 0

    def tgl_get_action_picking_tree_draft(self):
        action = self.env.ref('stock.action_picking_tree_all').read()[0]
        action['context'] = {'contact_display': 'partner_address', 'search_default_draft': 1}
        return action

    def tgl_get_action_picking_tree_partial_send(self):
        action = self.env.ref('stock.action_picking_tree_all').read()[0]
        action['context'] = {'contact_display': 'partner_address', 'search_default_partial_send': 1}
        return action

    def tgl_get_action_picking_tree_sended(self):
        action = self.env.ref('stock.action_picking_tree_all').read()[0]
        action['context'] = {'contact_display': 'partner_address', 'search_default_sended': 1}
        return action

    def tgl_get_action_picking_tree_partial_receipt(self):
        action = self.env.ref('stock.action_picking_tree_all').read()[0]
        action['context'] = {'contact_display': 'partner_address', 'search_default_partial_receipt': 1}
        return action

    def get_action_picking_tree_ready(self):
        action = super(StockPickingType, self).get_action_picking_tree_ready()
        if self.code == 'internal':
            action['context']['search_default_to_process'] = 1
            action['context']['search_default_available'] = 0
        return action
