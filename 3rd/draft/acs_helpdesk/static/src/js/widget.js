odoo.define('acs_gasavy_extension.web_timer', function (require) {
"use strict";
 
var core = require('web.core');
var AbstractField = require('web.AbstractField');
var field_registry = require('web.field_registry');
var time = require('web.time');
var utils = require('web.utils');

var _t = core._t;

var TicketTimeCounter = AbstractField.extend({
    supportedFieldTypes: [],

    willStart: function () {
        var self = this;
        var def = this._rpc({
            model: 'acs.support.ticket',
            method: 'search_read',
            domain: [
                ['id', '=', this.record.data.id],
            ],
        }).then(function (result) {
            if (self.mode === 'readonly') {
                var currentDate = new Date();
                self.duration = 0;
                _.each(result, function (data) {
                    self.duration += data.date_end ?
                        self._getDateDifference(data.date_start, data.date_end) :
                        self._getDateDifference(time.auto_str_to_date(data.date_start), currentDate);
                        self._startTimeCounter();
                });
            }
        });
        return $.when(this._super.apply(this, arguments), def);
    },

    destroy: function () {
        this._super.apply(this, arguments);
        clearTimeout(this.timer);
    },

    _getDateDifference: function (dateStart, dateEnd) {
        return moment(dateEnd).diff(moment(dateStart));
    },

    _startTimeCounter: function () {
        var self = this;
        clearTimeout(this.timer);
        this.timer = setTimeout(function () {
            self.duration += 1000;
            self._startTimeCounter();
        }, 1000);
        if (this.$el){
            this.$el.html($('<span>' + moment.utc(this.duration).format("HH:mm:ss") + '</span>'));
        }
    },
});


field_registry
    .add('web_time_counter', TicketTimeCounter);
});