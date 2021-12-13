# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons import decimal_precision as dp
from odoo.tools.float_utils import float_round
import operator as py_operator

OPERATORS = {
    '<': py_operator.lt,
    '>': py_operator.gt,
    '<=': py_operator.le,
    '>=': py_operator.ge,
    '=': py_operator.eq,
    '!=': py_operator.ne
}


class Product(models.Model):
    _inherit = "product.product"

    early_period_available = fields.Float(
        'Available of early period', compute='compute_early_period', search='_search_early_period_available',
        digits=dp.get_precision('Product Unit of Measure'))

    end_period_available = fields.Float(
        'Available of the end period', compute='compute_end_period', search='_search_end_period_available',
        digits=dp.get_precision('Product Unit of Measure'))

    incoming_qty_done = fields.Float('Import', compute='compute_during_period', search='_search_incoming_qty_done',
                                     digits=dp.get_precision('Product Unit of Measure'))
    outgoing_qty_done = fields.Float('Export', compute='compute_during_period', search='_search_outgoing_qty_done',
                                     digits=dp.get_precision('Product Unit of Measure'))

    @api.depends('stock_move_ids.product_qty', 'stock_move_ids.state')
    def compute_during_period(self):
        res = self._compute_quantities_from_to(self._context.get('lot_id'), self._context.get('owner_id'),
                                               self._context.get('package_id'), self._context.get('from_date'),
                                               self._context.get('to_date'))
        for product in self:
            # product.early_period_available = res[product.id]['early_period_available']
            product.incoming_qty_done = res[product.id]['incoming_qty_done']
            product.outgoing_qty_done = res[product.id]['outgoing_qty_done']
            # product.virtual_available = res[product.id]['virtual_available']

    @api.depends('stock_move_ids.product_qty', 'stock_move_ids.state')
    def compute_early_period(self):
        res = self._compute_quantities_date(self._context.get('lot_id'), self._context.get('owner_id'),
                                            self._context.get('package_id'), self._context.get('from_date'), False)
        for product in self:
            product.early_period_available = res[product.id]['early_period_available']
            # product.incoming_qty = res[product.id]['incoming_qty']
            # product.outgoing_qty = res[product.id]['outgoing_qty']
            # product.virtual_available = res[product.id]['virtual_available']

    @api.depends('stock_move_ids.product_qty', 'stock_move_ids.state')
    def compute_end_period(self):
        res = self._compute_quantities_date(self._context.get('lot_id'), self._context.get('owner_id'),
                                            self._context.get('package_id'), False, self._context.get('to_date'))
        for product in self:
            product.end_period_available = res[product.id]['end_period_available']
            # product.incoming_qty = res[product.id]['incoming_qty']
            # product.outgoing_qty = res[product.id]['outgoing_qty']
            # product.virtual_available = res[product.id]['virtual_available']

    def _compute_quantities_date(self, lot_id, owner_id, package_id, from_date=False, to_date=False):
        domain_quant_loc, domain_move_in_loc, domain_move_out_loc = self._get_domain_locations()
        domain_quant = [('product_id', 'in', self.ids)] + domain_quant_loc
        dates_in_the_past = False
        # only to_date as to_date will correspond to qty_available
        to_date = fields.Datetime.to_datetime(to_date)
        from_date = fields.Datetime.to_datetime(from_date)
        if to_date and to_date < fields.Datetime.now():
            dates_in_the_past = True

        if from_date and from_date < fields.Datetime.now():
            dates_in_the_past = True

        domain_move_in = [('product_id', 'in', self.ids)] + domain_move_in_loc
        domain_move_out = [('product_id', 'in', self.ids)] + domain_move_out_loc

        if lot_id is not None:
            domain_quant += [('lot_id', '=', lot_id)]
        if owner_id is not None:
            domain_quant += [('owner_id', '=', owner_id)]
            domain_move_in += [('restrict_partner_id', '=', owner_id)]
            domain_move_out += [('restrict_partner_id', '=', owner_id)]
        if package_id is not None:
            domain_quant += [('package_id', '=', package_id)]
        if dates_in_the_past:
            domain_move_in_done = list(domain_move_in)
            domain_move_out_done = list(domain_move_out)
        if from_date:
            domain_move_in += [('date', '=', from_date)]
            domain_move_out += [('date', '=', from_date)]
            #print(domain_move_in)
        if to_date:
            domain_move_in += [('date', '=', to_date)]
            domain_move_out += [('date', '=', to_date)]

        #print(domain_move_in)
        Move = self.env['stock.move']
        Quant = self.env['stock.quant']
        # domain_move_in_todo = [('state', 'in',
        #                        ('waiting', 'confirmed', 'assigned', 'partially_available'))] + domain_move_in
        # domain_move_out_todo = [('state', 'in',
        #                         ('waiting', 'confirmed', 'assigned', 'partially_available'))] + domain_move_out
        # moves_in_res = dict((item['product_id'][0], item['product_qty']) for item in
        #                   Move.read_group(domain_move_in_todo, ['product_id', 'product_qty'], ['product_id'],
        #                                    orderby='id'))
        # moves_out_res = dict((item['product_id'][0], item['product_qty']) for item in
        #                     Move.read_group(domain_move_out_todo, ['product_id', 'product_qty'], ['product_id'],
        #                                     orderby='id'))
        quants_res = dict((item['product_id'][0], item['quantity']) for item in
                          Quant.read_group(domain_quant, ['product_id', 'quantity'], ['product_id'], orderby='id'))

        if dates_in_the_past:
            # Calculate the moves that were done before now to calculate back in time (as most questions will be recent ones)
            if to_date:
                domain_move_in_done = [('state', '=', 'done'), ('date', '>', to_date)] + domain_move_in_done
                domain_move_out_done = [('state', '=', 'done'), ('date', '>', to_date)] + domain_move_out_done
            else:
                domain_move_in_done = [('state', '=', 'done'), ('date', '>', from_date)] + domain_move_in_done
                domain_move_out_done = [('state', '=', 'done'), ('date', '>', from_date)] + domain_move_out_done
            moves_in_res_past = dict((item['product_id'][0], item['product_qty']) for item in
                                     Move.read_group(domain_move_in_done, ['product_id', 'product_qty'], ['product_id'],
                                                     orderby='id'))
            moves_out_res_past = dict((item['product_id'][0], item['product_qty']) for item in
                                      Move.read_group(domain_move_out_done, ['product_id', 'product_qty'],
                                                      ['product_id'], orderby='id'))

        res = dict()
        #print(len(domain_move_out))
        for product in self.with_context(prefetch_fields=False):
            product_id = product.id
            rounding = product.uom_id.rounding
            res[product_id] = {}
            if dates_in_the_past:
                qty_available = quants_res.get(product_id, 0.0) - moves_in_res_past.get(product_id, 0.0) + moves_out_res_past.get(product_id, 0.0)
            else:
                qty_available = quants_res.get(product_id, 0.0)
            if to_date:
                res[product_id]['end_period_available'] = float_round(qty_available, precision_rounding=rounding)
            else:
                res[product_id]['early_period_available'] = float_round(qty_available, precision_rounding=rounding)
            # res[product_id]['incoming_qty'] = float_round(moves_in_res.get(product_id, 0.0), precision_rounding=rounding)
            # res[product_id]['outgoing_qty'] = float_round(moves_out_res.get(product_id, 0.0), precision_rounding=rounding)
            # res[product_id]['virtual_available'] = float_round(qty_available + res[product_id]['incoming_qty'] - res[product_id]['outgoing_qty'], precision_rounding=rounding)

        return res

    def _compute_quantities_from_to(self, lot_id, owner_id, package_id, from_date=False, to_date=False):
        domain_quant_loc, domain_move_in_loc, domain_move_out_loc = self._get_domain_locations()
        domain_quant = [('product_id', 'in', self.ids)] + domain_quant_loc
        # dates_in_the_past = False
        # only to_date as to_date will correspond to qty_available
        to_date = fields.Datetime.to_datetime(to_date)
        # if to_date and to_date < fields.Datetime.now():
        #   dates_in_the_past = True

        domain_move_in = [('product_id', 'in', self.ids)] + domain_move_in_loc
        domain_move_out = [('product_id', 'in', self.ids)] + domain_move_out_loc
        #print(domain_move_in)
        if lot_id is not None:
            domain_quant += [('lot_id', '=', lot_id)]
        if owner_id is not None:
            domain_quant += [('owner_id', '=', owner_id)]
            domain_move_in += [('restrict_partner_id', '=', owner_id)]
            domain_move_out += [('restrict_partner_id', '=', owner_id)]
        if package_id is not None:
            domain_quant += [('package_id', '=', package_id)]
        # if dates_in_the_past:
        #    domain_move_in_done = list(domain_move_in)
        #    domain_move_out_done = list(domain_move_out)
        if from_date:
            domain_move_in += [('date', '>=', from_date)]
            domain_move_out += [('date', '>=', from_date)]
            #print(domain_move_in)
        if to_date:
            domain_move_in += [('date', '<=', to_date)]
            domain_move_out += [('date', '<=', to_date)]

        # print(domain_move_in)
        Move = self.env['stock.move']
        # Quant = self.env['stock.quant']
        domain_move_in_todo = [('state', '=', ('done'))] + domain_move_in
        domain_move_out_todo = [('state', '=', ('done'))] + domain_move_out
        moves_in_res = dict((item['product_id'][0], item['product_qty']) for item in
                            Move.read_group(domain_move_in_todo, ['product_id', 'product_qty'], ['product_id'],
                                            orderby='id'))
        moves_out_res = dict((item['product_id'][0], item['product_qty']) for item in
                             Move.read_group(domain_move_out_todo, ['product_id', 'product_qty'], ['product_id'],
                                             orderby='id'))
        # quants_res = dict((item['product_id'][0], item['quantity']) for item in Quant.read_group(domain_quant, ['product_id', 'quantity'], ['product_id'], orderby='id'))
        # print(moves_in_res)
        # print(quants_res)
        # if dates_in_the_past:
        # Calculate the moves that were done before now to calculate back in time (as most questions will be recent ones)
        # domain_move_in_done = [('state', '=', 'done'), ('date', '>', to_date)] + domain_move_in_done
        # domain_move_out_done = [('state', '=', 'done'), ('date', '>', to_date)] + domain_move_out_done
        # moves_in_res_past = dict((item['product_id'][0], item['product_qty']) for item in Move.read_group(domain_move_in_done, ['product_id', 'product_qty'], ['product_id'], orderby='id'))
        # moves_out_res_past = dict((item['product_id'][0], item['product_qty']) for item in Move.read_group(domain_move_out_done, ['product_id', 'product_qty'], ['product_id'], orderby='id'))

        res = dict()
        # print(len(domain_move_out))
        for product in self.with_context(prefetch_fields=False):
            product_id = product.id
            rounding = product.uom_id.rounding
            res[product_id] = {}
            # res[product_id]['qty_available'] = float_round(qty_available, precision_rounding=rounding)
            res[product_id]['incoming_qty_done'] = float_round(moves_in_res.get(product_id, 0.0),
                                                               precision_rounding=rounding)
            res[product_id]['outgoing_qty_done'] = float_round(moves_out_res.get(product_id, 0.0),
                                                               precision_rounding=rounding)
            # res[product_id]['virtual_available'] = float_round(qty_available + res[product_id]['incoming_qty'] - res[product_id]['outgoing_qty'],precision_rounding=rounding)

        return res

    def _search_early_period_available(self, operator, value):
        # In the very specific case we want to retrieve products with stock available, we only need
        # to use the quants, not the stock moves. Therefore, we bypass the usual
        # '_search_product_quantity' method and call '_search_qty_available_new' instead. This
        # allows better performances.
        if value == 0.0 and operator == '>' and not ({'from_date', 'to_date'} & set(self.env.context.keys())):
            product_ids = self._search_qty_available_new(
                operator, value, self.env.context.get('lot_id'), self.env.context.get('owner_id'),
                self.env.context.get('package_id')
            )
            return [('id', 'in', product_ids)]
        return self._search_product_period(operator, value, 'early_period_available')

    def _search_product_period(self, operator, value, field):
        # TDE FIXME: should probably clean the search methods
        # to prevent sql injections
        if field not in ('early_period_available', 'end_period_available', 'incoming_qty_done'):
            raise UserError(_('Invalid domain left operand %s') % field)
        if operator not in ('<', '>', '=', '!=', '<=', '>='):
            raise UserError(_('Invalid domain operator %s') % operator)
        if not isinstance(value, (float, int)):
            raise UserError(_('Invalid domain right operand %s') % value)

        # TODO: Still optimization possible when searching virtual quantities
        ids = []
        for product in self.with_context(prefetch_fields=False).search([]):
            if OPERATORS[operator](product[field], value):
                ids.append(product.id)
        return [('id', 'in', ids)]

    def _search_end_period_available(self, operator, value):
        # TDE FIXME: should probably clean the search methods
        return self._search_product_period(operator, value, 'end_period_available')

    def _search_incoming_qty_done(self, operator, value):
        # TDE FIXME: should probably clean the search methods
        return self._search_product_period(operator, value, 'incoming_qty_done')

    def _search_outgoing_qty_done(self, operator, value):
        # TDE FIXME: should probably clean the search methods
        return self._search_product_period(operator, value, 'outgoing_qty_done')