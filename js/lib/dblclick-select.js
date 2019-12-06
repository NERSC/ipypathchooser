var controls = require('@jupyter-widgets/controls');
var _ = require('lodash');

/**
 *  Useful links:
 *  https://github.com/jupyter-widgets/ipywidgets/issues/1248#issuecomment-303808179
 *  https://github.com/jupyter-widgets/ipywidgets/blob/master/packages/controls/src/widget_selection.ts#L134#
 *  https://developer.mozilla.org/en-US/docs/Web/Events
*/

// Custom Model. Custom widgets models must at least provide default values
// for model attributes, including
//
//  - `_view_name`
//  - `_view_module`
//  - `_view_module_version`
//
//  - `_model_name`
//  - `_model_module`
//  - `_model_module_version`
//
//  when different from the base class.

// When serialiazing the entire widget state for embedding, only values that
// differ from the defaults will be specified.
// var HelloModel = widgets.DOMWidgetModel.extend({
//     defaults: _.extend(widgets.DOMWidgetModel.prototype.defaults(), {
//         _model_name : 'HelloModel',
//         _view_name : 'HelloView',
//         _model_module : 'ipypathchooser',
//         _view_module : 'ipypathchooser',
//         _model_module_version : '0.1.0',
//         _view_module_version : '0.1.0',
//         value : 'Hello World!'
//     })
// });

// An extension of SelectModel
// Ref: https://github.com/jupyter-widgets/ipywidgets/blob/master/packages/controls/src/widget_selection.ts#L123
// Adds a place to store a double-clicked element
var DoubleClickSelectModel = controls.SelectModel.extend({
    defaults: _.extend(controls.SelectModel.prototype.defaults(), {
        _model_name : 'DoubleClickSelectModel',
        _view_name : 'DoubleClickSelectView',
        _model_module : 'ipypathchooser',
        _view_module : 'ipypathchooser',
        _model_module_version : '0.1.0',
        _view_module_version : '0.1.0',
        dblclick: '',
    })
});

// fiddle: https://jsfiddle.net/wemhsLf5/

// An extension of SelectView
// Ref: https://github.com/jupyter-widgets/ipywidgets/blob/master/packages/controls/src/widget_selection.ts#L134
var DoubleClickSelectView = controls.SelectView.extend({
    _updateOptions: function() {
        this.listbox.textContent = '';
        var items = this.model.get('_options_labels');
        var icons = this.model.get('icons');
        for (var i = 0; i < items.length; i++) {
            var item = items[i];
            var option = document.createElement('option');
            var icon = icons[i];
            option.textContent = icon ? icon + ' ' : '';
            option.textContent += item.replace(/ /g, '\xa0'); // space -> &nbsp;
            option.setAttribute('data-value', encodeURIComponent(item));
            option.value = item;
            this.listbox.appendChild(option);
        }
    },

    render: function() {
        connsole.log('rendering...')
        this.render();
        console.log('this: ', this);
        console.log('el: ', this.el);
        this.el.listbox.style.fontFamily = 'FontAwesome, sans-serif';
        // this.value_changed();
        // this.model.on('change:value', this.value_changed, this);
    },

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

    // value_changed: function() {
    //     this.el.textContent = this.model.get('value');
    // }
});

// Custom View. Renders the widget model.
// var HelloView = widgets.DOMWidgetView.extend({
//     render: function() {
//         this.value_changed();
//         this.model.on('change:value', this.value_changed, this);
//     },

//     value_changed: function() {
//         this.el.textContent = this.model.get('value');
//     }
// });


module.exports = {
    DoubleClickSelectModel : DoubleClickSelectModel,
    DoubleClickSelectView : DoubleClickSelectView,
};
