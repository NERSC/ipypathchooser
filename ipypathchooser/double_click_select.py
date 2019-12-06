# Third-party
from traitlets import Unicode, Int, List
from ipywidgets import Select, register
# Local
from . import _version

# SelectMultiple is chosen over Select because of a bug in macOS relating to displaying the icons otherwise
# Ref: https://stackoverflow.com/a/36743356

@register
class DoubleClickSelect(Select):
    """
    Extends: https://github.com/jupyter-widgets/ipywidgets/blob/master/ipywidgets/widgets/widget_selection.py#L486
    """
    _view_name = Unicode('DoubleClickSelectView').tag(sync=True)
    _view_module = Unicode('ipypathchooser').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)

    _model_name = Unicode('DoubleClickSelectModel').tag(sync=True)
    _model_module = Unicode('ipypathchooser').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)

    # A list of Font Awesome icons in unicode, or ' '*4
    icons = List(trait=Unicode, default_value=[], help='A list of icons to display with items').tag(sync=True)

    # Just like a Select's selected index, but set upon `dblclick` event
    dblclick = Int(None, help="dblclick index", allow_none=True).tag(sync=True)

    def __init__(self, **kwargs):
        # Call Select super class __init__
        super().__init__(**kwargs)
