odoo.define('action_manager_stock_reports.ActionManager', function (require) {
"use strict";

var ActionManager = require('web.ActionManager');
var crash_manager = require('web.crash_manager');
var framework = require('web.framework');
var session = require('web.session');

ActionManager.include({
    /**
     * Overrides to handle the 'ir_actions_stock_report_download' actions.
     *
     * @override
     * @private
     */
    _handleAction: function (action, options) {
        if (action.type === 'ir_actions_stock_report_download') {
            framework.blockUI();
            var def = $.Deferred();

            session.get_file({
                url: '/action_report_print',
                data: action.data,
                success: def.resolve.bind(def),
                error: function () {
                    crash_manager.rpc_error.apply(crash_manager, arguments);
                    def.reject();
                },
                complete: framework.unblockUI,
            });
            return def;
        }
        return this._super.apply(this, arguments);
    },
});

});
