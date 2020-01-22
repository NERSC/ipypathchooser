from ._version import version_info, __version__

from .pathchooser import *

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'ipypathchooser',
        'require': 'ipypathchooser/extension'
    }]
