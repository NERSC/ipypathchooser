var controls = require('@jupyter-widgets/controls');
var _ = require('lodash');

// An extension of SelectModel
// Adds a place to store a double-clicked element's index
// Ref: https://github.com/jupyter-widgets/ipywidgets/blob/master/packages/controls/src/widget_selection.ts#L123
var DoubleClickSelectModel = controls.SelectModel.extend({
    defaults: _.extend(controls.SelectModel.prototype.defaults(), {
        _view_name : 'DoubleClickSelectView',
        _view_module : 'ipypathchooser',
        _view_module_version : '0.1.0',
        _model_name : 'DoubleClickSelectModel',
        _model_module : 'ipypathchooser',
        _model_module_version : '0.1.0',
        dblclick: null,
    })
});

// An extension of SelectView
// Ref: https://github.com/jupyter-widgets/ipywidgets/blob/master/packages/controls/src/widget_selection.ts#L134
var DoubleClickSelectView = controls.SelectView.extend({
    _updateOptions: function() {
        this.listbox.textContent = '';
        var items = this.model.get('_options_labels');
        // The icons are expected to be FontAwesome icons in unicode
        // Ref: https://jsfiddle.net/9vw6nf0b/
        var icons = this.model.get('icons');
        for (var i = 0; i < items.length; i++) {
            var item = items[i];
            var option = document.createElement('option');
            var icon = icons[i];
            if (icon !== undefined) {
                option.textContent = icon + '\xa0\xa0';
            }
            // space -> &nbsp;
            option.textContent += item.replace(/ /g, '\xa0');
            option.setAttribute('data-value', encodeURIComponent(item));
            option.value = item;
            this.listbox.appendChild(option);
        }
    },

    render: function() {
        controls.SelectView.prototype.render.call(this);
        this.listbox.style.fontFamily = 'FontAwesome, sans-serif';
    },

    // dblclick is a standard event
    // Ref: https://developer.mozilla.org/en-US/docs/Web/Events
    events: function() {
        var events = controls.SelectView.prototype.events();
        _.extend(events, {
            'dblclick': '_handle_dblclick',
        });
        return events;
    },

    _handle_dblclick: function() {
        this.model.set('dblclick', this.listbox.selectedIndex, {updated_view: this});
        this.touch();
    },
});

module.exports = {
    DoubleClickSelectModel : DoubleClickSelectModel,
    DoubleClickSelectView : DoubleClickSelectView,
};
