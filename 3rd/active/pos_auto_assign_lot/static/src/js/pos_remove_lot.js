odoo.define('pos_auto_assign_lot.pos_remove_lot_selection', function (require) {
	"use strict";
	
    var core = require('web.core');
    var pos_model = require('point_of_sale.models');
    var models = pos_model.PosModel.prototype.models;
    var PosModelSuper = pos_model.PosModel;
    var OrderSuper = pos_model.Order;
    var rpc = require('web.rpc');

    pos_model.Order = pos_model.Order.extend({
        display_lot_popup: function() {
	        return true;
    	},
    });
    
    pos_model.Orderline = pos_model.Orderline.extend({
        
        has_valid_product_lot: function(){
            return true;
        },
    });
    
});
