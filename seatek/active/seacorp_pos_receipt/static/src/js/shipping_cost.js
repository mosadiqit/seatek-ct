odoo.define('seacorp_pos_receipt.shipping_cost', function (require) {
"use strict";

var core = require('web.core');
var screens = require('point_of_sale.screens');

var _t = core._t;

var ShippingCostButton = screens.ActionButtonWidget.extend({
    template: 'ShippingCostButton',
    button_click: function(){
        var self = this;
        this.gui.show_popup('number',{
            'title': _t('Shipping Cost'),
            'value': this.pos.config.shipping_cost,
            'confirm': function(val) {
                self.apply_shipping_cost(val);
            },
        });
    },
    apply_shipping_cost: function(pc) {
        var order    = this.pos.get_order();
        console.log('order', order);
        var lines    = order.get_orderlines();
        console.log('lines', lines);
        var product  = this.pos.db.get_product_by_id(this.pos.config.shipping_product_id[0]);
        console.log('product', product);
        if (product === undefined) {
            this.gui.show_popup('error', {
                title : _t("No shipping product found"),
                body  : _t("The shipping product seems misconfigured. Make sure it is flagged as 'Can be Sold' and 'Available in Point of Sale'."),
            });
            return;
        }

        // Remove existing shipping charge
        var i = 0;
        while ( i < lines.length ) {
            if (lines[i].get_product() === product) {
                order.remove_orderline(lines[i]);
            } else {
                i++;
            }
        }

        // Add shipping_cost
        var shipping_cost = pc;

        if( shipping_cost > 0 ) {
            order.add_product(product, { price: shipping_cost });
        }

    },
});

screens.define_action_button({
    'name': 'shipping_cost',
    'widget': ShippingCostButton,
    'condition': function(){
        return this.pos.config.enable_shipping_cost && this.pos.config.shipping_product_id;
    },
});

return {
    ShippingCostButton: ShippingCostButton,
}

});
