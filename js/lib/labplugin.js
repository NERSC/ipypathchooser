var plugin = require('./index');
var base = require('@jupyter-widgets/base');

module.exports = {
  id: 'ipypathchooser',
  requires: [base.IJupyterWidgetRegistry],
  activate: function(app, widgets) {
      widgets.registerWidget({
          name: 'ipypathchooser',
          version: plugin.version,
          exports: plugin
      });
  },
  autoStart: true
};

