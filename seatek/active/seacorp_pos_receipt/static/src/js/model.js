odoo.define("seacorp_pos_receipt.model", function (require) {
    "use strict";
    var models = require('point_of_sale.models');    
    var core = require('web.core');
    var _t = core._t;    
    var session = require('web.session');
    var rpc = require('web.rpc');

    var field_utils = require('web.field_utils');

    var _super_PosModel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        get_model: function (_name) {
            var _index = this.models.map(function (e) {
                return e.model;
            }).indexOf(_name);
            if (_index > -1) {
                return this.models[_index];
            }
            return false;
        },
        initialize: function (session, attributes) {
            var self = this;            
            // var company_model = this.get_model('res.company');
            // company_model.fields.push('street');  
            // company_model.fields.push('street2');  
            // company_model.fields.push('city');  

            var account_tax_model = this.get_model('account.tax');
            account_tax_model.fields.push('description');
            
            _super_PosModel.initialize.apply(this, arguments);          

        },        
        get_config: function () {
            return this.config;
        },        
      
    });

    models.Order = models.Order.extend({
        get_shippng_cost : function() {
            var order    = this.pos.get_order();
            var lines    = order.get_orderlines();
            var product  = this.pos.db.get_product_by_id(this.pos.config.shipping_product_id[0]);

            var i = 0;
            while ( i < lines.length ) {
                if (lines[i].get_product() === product) {
                    return lines[i].get_unit_price();   
                } else {
                    i++;
                }
            }
            return 0;
        },        
        tgl_get_discount_str : function() {
            var self = this;
            var order    = this.pos.get_order();
            var lines    = order.get_orderlines();
            var product  = this.pos.db.get_product_by_id(this.pos.config.shipping_product_id[0]);
            var result = [];

            _.each(lines, function(line){
                _.each(self.pos.discounts, function(discount){
                    var product = self.pos.db.product_by_id[discount.product_id[0]];
                    if (product === line.get_product()) {
                        result.push(discount.amount + '%');
                    }
                })
                
            });
            return result.join(',');
        },
        tgl_get_discount_value : function() {
            var self = this;
            console.log('self.pos.discounts', self.pos.discounts);
            var order    = this.pos.get_order();
            var lines    = order.get_orderlines();
            var product  = this.pos.db.get_product_by_id(this.pos.config.shipping_product_id[0]);
            var result = 0;
            _.each(lines, function(line){
                _.each(self.pos.discounts, function(discount){
                    var product = self.pos.db.product_by_id[discount.product_id[0]];
                    if (product === line.get_product()) {
                        result += line.get_unit_price(); 
                    }
                })
                
            });
            return result;
        },

        /*GET ODER REF IN BILL*/
        get_order_ref : function(){
            var indexMaxOrder =  this.pos.db.get_pos_orders().length-1;
            var result = 0;
            var nameTemp = this.pos.db.get_pos_orders()[indexMaxOrder].name
            var prefix = nameTemp.split('/')[0]
            var sequenceTemp = nameTemp.split('/')[1];
            var sequence_number = Number(sequenceTemp)+1;
            var sequence_string = sequence_number.toString()
            var leng = sequenceTemp.length;
            var sequence = sequence_string.padStart(leng, '0')
            return prefix+'/'+sequence;
        },

        // Replace Oder number sequence in point of sale
//        generate_unique_id: function() {
//        // Generates a public identification number for the order.
//        // The generated number must be unique and sequential. They are made 12 digit long
//        // to fit into EAN-13 barcodes, should it be needed
//
//            function zero_pad(num,size){
//                var s = ""+num;
//                while (s.length < size) {
//                    s = "0" + s;
//                }
//                return s;
//            }
//            var today = new Date();
//            var mm = today.getMonth()+1;
//            var is_string_date =String(today.getYear())-100+''+mm+''+today.getDate();
//            return is_string_date +'-'+
//                   zero_pad(this.pos.config.sea_pos_code,3) +'-'+
//                   zero_pad(this.sequence_number,4);
//        },
    });

    models.Orderline = models.Orderline.extend({
        get_taxes_label : function() {
            var taxes_ids = this.get_product().taxes_id;
            var taxes = "";
            for (var i = 0; i < taxes_ids.length; i++) {
                // console.log('this.pos.taxes_by_id[taxes_ids[i]]', this.pos.taxes_by_id[taxes_ids[i]]);
                taxes += "("+this.pos.taxes_by_id[taxes_ids[i]].description+")" ;
            }
            return taxes;
        },
    });

});