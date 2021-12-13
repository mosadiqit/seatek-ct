odoo.define("seacorp_pos_search_unaccent.main", function (require) {
    "use strict";

    var models = require('point_of_sale.models');    
    var core = require('web.core');    
    var _t = core._t;    
    var session = require('web.session');
    var rpc = require('web.rpc');
    var db = require('point_of_sale.DB');
    var _super_db = db.prototype;

    var _super_PosModel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        
        initialize: function (session, attributes) {
            this.get_model('product.product').fields.push('name_unaccent');
            this.get_model('res.partner').fields.push('name_unaccent');
            _super_PosModel.initialize.apply(this, arguments);          

        },        
    });

    _super_db._partner_search_string = function (partner) {
        var str = partner.name;
        if (partner.name_unaccent) {
            str += '|' + partner.name_unaccent;
        }
        if (partner.ref) {
            str += '|' + partner.ref;
        }
        if (partner.barcode) {
            str += '|' + partner.barcode;
        }
        if (partner.address) {
            str += '|' + partner.address;
        }
        if (partner.phone) {
            str += '|' + partner.phone.split(' ').join('');
        }
        if (partner.mobile) {
            str += '|' + partner.mobile.split(' ').join('');
        }
        if (partner.email) {
            str += '|' + partner.email;
        }
        str = '' + partner.id + ':' + str.replace(':', '') + '\n';
        return str;
    };

    _super_db._product_search_string = function (product) {
        var str = product.display_name;
        if (product.name_unaccent) {
            str += '|' + product.name_unaccent;
        }
        if (product.barcode) {
            str += '|' + product.barcode;
        }
        if (product.default_code) {
            str += '|' + product.default_code;
        }
        if (product.description) {
            str += '|' + product.description;
        }
        if (product.description_sale) {
            str += '|' + product.description_sale;
        }
        str  = product.id + ':' + str.replace(/:/g,'') + '\n';
        return str;
    };

});