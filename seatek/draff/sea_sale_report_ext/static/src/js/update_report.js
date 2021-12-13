odoo.define('sea_sale_report_ext.report_update', function(require) {
    "use strict";

    var core = require('web.core');
    var ListController = require('web.ListController');
    var rpc = require('web.rpc');
    var session = require('web.session');
    var _t = core._t;
    ListController.include({
        renderButtons: function ($node) {
            this._super.apply(this, arguments);
            if (this.$buttons) {
                this.$buttons.find('.oe_action_update').click(this.proxy('report_update'));
            }
        },
        report_update: function () {
            var self = this
            var user = session.uid;
            rpc.query({
                model: 'sea_sale_report_ext.report_line',
                method: 'report_update',
                args: [[user], { 'id': user }],
            })
        }
    });
});