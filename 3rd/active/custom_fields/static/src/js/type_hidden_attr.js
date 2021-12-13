odoo.define('custom_fields.type_hidden_attr', function(require) {
    'use strict';

    var base = require('web_editor.base');

    function _redefineVisibility(InstanceType) {
        // The method to change attributes of input fields when type is changed
        var FieldsCheckIDS = $('.type_visibility_depend');
        for (var i = 0; i < FieldsCheckIDS.length; ++i) {
            var field = FieldsCheckIDS[i];
            var inputs = field.getElementsByClassName("o_website_form_input");
            var input = inputs[0];
            var AvailableTypes = input.getAttribute("invisible");

            if (AvailableTypes) {
                var AvailableTypesArray = AvailableTypes.split(',');
                if (AvailableTypesArray.indexOf(InstanceType) > -1) {
                    field.removeAttribute("style");
                    // In case of double change a field should become required back
                    if (input.getAttribute("needrequired") == "True") {
                        input.setAttribute("required", "True");
                    };
                }
                else {
                    field.setAttribute("style", "display: none;");
                    if (input.getAttribute("required") == "True") {
                        input.removeAttribute("required");
                        input.setAttribute("needrequired", "True");
                    }
                };
            };
        };
    };

    base.ready().then(function () {
        // Change input attributes after loading page and in case type is changed
        var indexEv = $('.select_type_input');
        if (indexEv.length !== 0) {_redefineVisibility(indexEv[0].value);}
        else {_redefineVisibility(0);};
        $('.select_type_input').on('change', function (ev) {
            var InstanceType = ev.currentTarget.value;
            _redefineVisibility(InstanceType);
        });
    });

});
