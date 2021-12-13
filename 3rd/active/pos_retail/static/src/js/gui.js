odoo.define('pos_retail.gui', function (require) {
    "use strict";
    var gui = require('point_of_sale.gui');

    gui.Gui.include({
        show_popup: function (name, options) {
            if (!this.popup_instances[name]) {
                console.error('PopUp name ' + name + ' not found');
                return null;
            }
            if (!this.pos.config.is_customer_screen) {
                this._super(name, options);
            } else {
                return null;
            }
            this.remove_keyboard()

        },
        add_keyboard: function (screen_name) {
            var products_screen = this.screen_instances['products'];
            var is_customer_screen = this.pos.config.is_customer_screen;
            if (!products_screen || is_customer_screen) {
                return null;
            } else {
                var order_widget = products_screen.order_widget;
                if (!order_widget) {
                    console.error('could not find order widget');
                }
            }
        },
        remove_keyboard: function () {
            var products_screen = this.screen_instances['products'];
            if (!products_screen) {
                return res;
            }
        },
        show_screen: function (screen_name, params, refresh, skip_close_popup) {
            if (screen_name != 'products' || this.pos.config.mobile_responsive) {
                $('.pos-branding').addClass('oe_hidden');
                $('.pos .pos-rightheader').css('left', '0px');
            } else {
                $('.pos-branding').removeClass('oe_hidden');
                $('.pos .pos-rightheader').css('left', '600px');
            }
            this._super(screen_name, params, refresh, skip_close_popup);
            if (!this.pos.config.mobile_responsive) {
                this.add_keyboard(screen_name);
            }

        },
        close_popup: function () {
            this._super();
            if (!this.pos.config.mobile_responsive) {
                this.add_keyboard(this.get_current_screen());
            }
        },
        set_default_screen: function (name) {
            this._super(name);
            if (!this.pos.config.mobile_responsive) {
                var products_screen = this.screen_instances['products'];
                if (!products_screen) {
                    return res;
                } else {
                    var order_widget = products_screen.order_widget;
                    if (!order_widget) {
                        return res;
                    }
                }
            }

        },
    });
});