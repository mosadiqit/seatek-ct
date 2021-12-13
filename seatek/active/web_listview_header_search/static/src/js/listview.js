odoo.define('web_listview_header_search.main', function (require) {
"use strict";

var time        = require('web.time');
var core        = require('web.core');
var data        = require('web.data');
var session     = require('web.session');
var utils       = require('web.utils');
var _t = core._t;
var _lt = core._lt;
var QWeb = core.qweb;
var config      = require('web.config');

function is_mobile() {
    return config.device.size_class <= config.device.SIZES.XS;
}

var SearchView          = require('web.SearchView');
var ListController      = require('web.ListController');
var ListRenderer        = require('web.ListRenderer');
var KanbanController = require('web.KanbanController');
var KanbanRenderer = require('web.KanbanRenderer');

SearchView.include({
    build_search_data: function (noDomainEvaluation) {
        var res = this._super(noDomainEvaluation);
        if (this.tgl_domain) 
            res.domains = res.domains.concat(this.tgl_domain);

        return res;
    },
});

ListController.include({
    renderButtons: function ($node) {
        var self = this;
        this._super.apply(this, arguments);
        this.$buttons.append(`
            <button class="btn btn-sm btn-default tgl_search_header_btn">
                Bỏ lọc <i class="fa fa-search"></i>
            </button>
        `)
        this.$buttons.find('.tgl_search_header_btn').click(function(event){
            var searchView = self.searchView;
            searchView.tgl_key = null;
            searchView.tgl_domain = null;
            searchView.selected_field = null;
            searchView.query.trigger('reset');
            // $('.tgl_search_header').toggleClass('hidden')
        });
    },  

});


ListRenderer.include({
    events: _.extend(ListRenderer.prototype.events, {
        'change .tgl_search_header': 'tgl_search_header',
        'keyup .tgl_search_header': 'tgl_search_header',
        'click .tgl_header_content': '_onSortColumn',
        'click .o_selection_menu .dropdown-item' : '_onClickAddSelected',
        'click .o_selection_menu .dropdown-item.selected' : '_onClickRmvSelected',
        'hidden.bs.dropdown .qth_search_selection' : '_onHiddenSelectionMenu',
        'show.bs.dropdown .qth_search_selection' : '_onShowSelectionMenu',

    }),

    _onShowSelectionMenu: function(event) {
        var name = $(event.currentTarget).data('name'),
            field = this.state.fields[name],
            type = field.type,
            searchView = this.getParent().searchView,
            items = $(event.currentTarget).find('.o_selection_menu .dropdown-item');

        event.stopPropagation();
        if (!searchView.selected_field) searchView.selected_field = {};
        if (!searchView.selected_field[name]) {
            searchView.selected_field[name] = {};
            $(event.currentTarget).find('.o_selection_menu .o_menu_item_all .dropdown-item').click();
        }
        else {
            if (searchView.selected_field[name][""] === 1) {
                items.addClass('selected');
            } else {
                var count_key0 = 0;
                _.each(items, function(item){
                    if (searchView.selected_field[name][$(item).data('key')] === 1)
                        $(item).addClass('selected');
                    else 
                       count_key0++; 
                })
                if (count_key0 === items.length)
                    $(event.currentTarget).find('.o_selection_menu .o_menu_item_all .dropdown-item').click();
            }
        }
    },

    _onHiddenSelectionMenu: function(event) {
        var name = $(event.currentTarget).data('name'),
            value = [],
            field = this.state.fields[name],
            type = field.type,
            searchView = this.getParent().searchView,
            select_items = $(event.currentTarget).find('.o_selection_menu .dropdown-item.selected')

        event.stopPropagation();

        _.each(select_items, function(item) {
            if ($(item).data('key') !== "") 
                value.push($(item).data('key'));
        });
        if (!searchView.tgl_key) {
            searchView.tgl_key = {}
        }
        searchView.tgl_key[name] = {
            'value': value,
            'type': type,
        };

        this.tgl_build_search_domain();
    },

    _onClickAddSelected: function(event) {
        if ($(event.currentTarget).hasClass('selected')) return ;

        var currenNode = $(event.currentTarget),
            parentNode = $(currenNode[0].parentNode),
            searchView = this.getParent().searchView,
            name = currenNode.data('name'),
            key = currenNode.data('key');

        event.stopPropagation();
        if (key === "") {
            searchView.selected_field[name][key] = 1;
            $(parentNode[0].parentNode).find('.dropdown-item.selected').removeClass('selected');
            $(parentNode[0].parentNode).find('.dropdown-item').addClass('selected');
            _.each($(parentNode[0].parentNode).find('.dropdown-item'), function(item){
                searchView.selected_field[name][$(item).data('key')] = 1;
            })
        } else {
            currenNode.addClass('selected'); 
            searchView.selected_field[name][key] = 1;
            var count_selected = $(parentNode[0].parentNode).find('.dropdown-item.selected').length,
                count_all = $(parentNode[0].parentNode).find('.dropdown-item').length,
                $item_all = $(parentNode[0].parentNode).find('.o_menu_item_all .dropdown-item');

            if ((count_selected+1 === count_all) && (!$item_all.hasClass('selected'))) {
                searchView.selected_field[name][""] = 1;
                $item_all.addClass('selected');
            }
        }
    },

    _onClickRmvSelected: function(event) {
        if (!$(event.currentTarget).hasClass('selected')) return ;
        var currenNode = $(event.currentTarget),
            parentNode = $(currenNode[0].parentNode),
            searchView = this.getParent().searchView,
            name = currenNode.data('name'),
            key = currenNode.data('key');

        event.stopPropagation();
        if (key === "") {
            searchView.selected_field[name][key] = 0;
            $(parentNode[0].parentNode).find('.dropdown-item.selected').removeClass('selected');
            _.each($(parentNode[0].parentNode).find('.dropdown-item'), function(item){
                searchView.selected_field[name][$(item).data('key')] = 0;
            })
        } else {
            currenNode.removeClass('selected');
            searchView.selected_field[name][key] = 0;
            searchView.selected_field[name][""] = 0;
            $(parentNode[0].parentNode).find('.o_menu_item_all .dropdown-item.selected').removeClass('selected');
        }
    },

    tgl_build_search_domain: function() {
        var tgl_domain = [],
            searchView = this.getParent().searchView;

        _.each(searchView.tgl_key, function(value, key, list){
            if (!value || value == '') {
                delete searchView.tgl_key[key];
            } else if (value.type == 'monetary' || value.type == 'integer' || value.type == 'float') {
                var v = value.value;
                if (v.includes('>=')) {
                    tgl_domain.push([key, '>=', parseFloat(v.split('>=')[1])]);
                } else if (v.includes('<=')) {
                    tgl_domain.push([key, '<=', parseFloat(v.split('<=')[1])]);
                } else if (v.includes('>')) {
                    tgl_domain.push([key, '>', parseFloat(v.split('>')[1])]);
                } else if (v.includes('<')) {
                    tgl_domain.push([key, '<', parseFloat(v.split('<')[1])]);
                } else if (v.includes('-')) {
                    var range_value = v.split('-');
                    tgl_domain.push([key, '>=', parseFloat(range_value[0])]);
                    tgl_domain.push([key, '<=', parseFloat(range_value[1])]);
                }

            } else if (value.type == 'date' || value.type == 'datetime') {
                tgl_domain.push([key,'>=',value.value[0]]);
                tgl_domain.push([key,'<=',value.value[1]]);
            }            
            else if (value.type == 'selection'){
                for (var i = 0; i < (value.value.length - 1); i++)
                    tgl_domain.push('|');
                _.each(value.value, function(val) {
                    tgl_domain.push([key,'ilike',val]);
                });
            } else {
                tgl_domain.push([key,'ilike',value.value]);
            }                

        });

        searchView.tgl_domain = [tgl_domain];
        searchView.query.trigger('reset');

    },

    tgl_search_header: function(event) {
        if (
            ((event.key === "Enter") && (event.type === "keyup")) || 
            ((event.type !== "keyup"))
            )  {
            var name = $(event.currentTarget).data('name'),
                value = $(event.currentTarget).val(),
                tgl_domain = [],
                field = this.state.fields[name],
                type = field.type,
                searchView = this.getParent().searchView;
            event.stopPropagation();

            if (!searchView.tgl_key) {
                searchView.tgl_key = {}
            }
            searchView.tgl_key[name] = {
                'value': value,
                'type': type,
            };
            this.tgl_build_search_domain();
        };
    },

    _renderHeader: function (isGrouped) {
        var $thead = this._super(isGrouped);
        var $tr = $('<tr>')
        var $tr_search = $('<tr>').append(_.map(this.columns, this._renderSearchHeaderCell.bind(this)));
        if (this.getParent() && this.getParent().viewType == 'list') {
            var count_empty = $thead.find('tr:last th').length - $tr_search.find('th').length
            for (var i=0; i < count_empty; i++) {
                $tr_search.prepend($('<th>'));
            }
        }
        return $thead.append($tr_search);
    },

    _renderSearchHeaderCell: function (node) {
        var self = this,
            name = node.attrs.name,
            searchView = this.getParent().searchView,
            value = '',
            res = $('<th>');

        if (node.attrs.widget == 'handle') return ;

        if (!searchView) return ;

        var field = this.state.fields[name];
        if (!field) return;
        var type = field.type;
        if (!type) return;
        if (field.sortable == false) {
            return res.append(`
            <div class="tgl_search_header_container">
            </div>`);
        }
        
        
        if (searchView.tgl_key && searchView.tgl_key[name]) {
            value = searchView.tgl_key[name].value;
            if (type == 'datetime' || type == 'date') { 
                value = searchView.tgl_key[name].display_value;
            }
        }

        res.append(`
            <div class="tgl_search_header_container">
                <input class="tgl_search_header o_input" type="text" placeholder="Tìm..." id="${name}" value="${value}" data-name="${name}"/>
            </div>`
        );
        
        var $tgl_search_header_container = res.find('.tgl_search_header_container');
        var server_datetime_format = 'YYYY-MM-DD HH:mm:ss';

        if (type == 'selection') {
            var Field = core.search_filters_registry.getAny([type, "char"]);
            var field_value = new Field(this, field);
            $tgl_search_header_container.html('');
            var field_to_render = $(QWeb.render('QTH.selection', {
                'fields': field_value.field.selection,
                'name': name,
            }))

            field_to_render.val(value);
            field_to_render.appendTo($tgl_search_header_container);
        }


        if (type == 'datetime' || type == 'date') {
            var l10n                = _t.database.parameters,
            datetime_format         = time.getLangDatetimeFormat();
            $tgl_search_header_container.html('');

            $tgl_search_header_container.append(
                `<input class="tgl_range_search_header o_input" placeholder="Tìm..." type="text" value="${value}" data-name="${name}"/>`
            );
            $tgl_search_header_container.find('.tgl_range_search_header').daterangepicker({
                showDropdowns: true,
                timePicker: false,
                timePickerIncrement: 5,
                timePicker24Hour: true,
                startDate: moment().startOf('day'),
                endDate: moment().startOf('day'),
                locale : {
                    format: datetime_format.substring(0, 10),
                    applyLabel: _t('Áp dụng'),
                    cancelLabel: _t('Hủy'),
                    customRangeLabel: _t('Tùy chỉnh'),
                },
                ranges: {
                    'Hôm nay': [moment().startOf('day'), moment().endOf('day')],
                    'Hôm qua': [moment().startOf('day').subtract(1, 'days'), moment().endOf('day').subtract(1, 'days')],
                    '7 ngày gần đây': [moment().startOf('day').subtract(6, 'days'), moment().endOf('day')],
                    '30 ngày gần đây': [moment().startOf('day').subtract(29, 'days'), moment().endOf('day')],
                    'Tháng này': [moment().startOf('month'), moment().endOf('month')],
                    'Tháng trước': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
                }
            });
            var tgl_time_field = $tgl_search_header_container.find('.tgl_range_search_header');
            tgl_time_field.val(value);
            tgl_time_field.on('cancel.daterangepicker', function(ev, picker) {
                tgl_time_field.val('');
                if (searchView.tgl_key) {
                    delete searchView.tgl_key[name];
                    self.tgl_build_search_domain();
                }
            });
            tgl_time_field.on('apply.daterangepicker', function(ev, picker) {

                var start = moment(picker.startDate),
                    end = moment(picker.endDate),
                    display_value = start.format(datetime_format.substring(0, 10)) + '-' + end.format(datetime_format.substring(0, 10));

                start.subtract(session.getTZOffset(start.format(server_datetime_format)), 'minutes');
                end.subtract(session.getTZOffset(end.format(server_datetime_format)), 'minutes');

                if (!searchView.tgl_key) {
                    searchView.tgl_key = {}
                }

                searchView.tgl_key[name] = {
                    'display_value': display_value,
                    'value': [start.format(server_datetime_format), end.format(server_datetime_format)],
                    'type': type,
                };
                self.tgl_build_search_domain();
            });
        };
        return res;
    },

});


});