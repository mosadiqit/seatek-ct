odoo.define('web_export_ux.main', function (require) {
    "use strict";

    var Sidebar = require('web.Sidebar');
    var session = require('web.session');
    var crash_manager = require('web.crash_manager');
    var framework = require('web.framework');
    var pyUtils = require('web.py_utils');
    var core = require('web.core');
    var QWeb = core.qweb;

    var _t = core._t;

    Sidebar.include({

        _redraw: function () {
            var self = this;
            this._super.apply(this, arguments);
            if (self.getParent().renderer.viewType === 'list') {
                session.user_has_group('web_export_ux.group_disallow_quick_export').then(function (has_group) {
                    if (has_group) {
                        return;
                    }
                    self._rpc({
                        model: 'ir.exports',
                        method: 'search_read',
                        fields: ['name'],
                        domain: [['resource', '=', self.env.model]]
                    }).then(function (export_list) {
                        var export_btn = self.$el.find('.export_treeview_xls');
                        if (!export_btn.length) {
                            var WebQuickExport =  QWeb.render('WebQuickExport', {widget: self, 'export_list': export_list});
                            self.$el.find('.o_dropdown').parent().append(WebQuickExport);
                            $('.tgl_quick_export_btn').click(function(event){
                                var export_id = $(event.currentTarget).data('id');
                                self._rpc({
                                    route: '/web/export/namelist',
                                    params: {
                                        model: self.env.model,
                                        export_id: export_id,
                                    },
                                })
                                .then(function(exported_fields) {
                                    exported_fields.unshift({name: 'id', label: _t('External ID')});
                                    framework.blockUI();
                                    self.getSession().get_file({
                                        url: '/web/export/xls',
                                        data: {data: JSON.stringify({
                                            model: self.env.model,
                                            fields: exported_fields,
                                            ids: self.getParent().getSelectedIds(),
                                            domain: [],
                                            context: {},
                                            import_compat: true,
                                        })},
                                        complete: framework.unblockUI,
                                        error: crash_manager.rpc_error.bind(crash_manager),
                                    });
                                });

                            });

                        }
                    }); 
                }); 
            }
        },

    });
});
