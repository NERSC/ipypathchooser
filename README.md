ipypathchooser
===============================

An ipywidget for choosing a path (file or directory) interactively

Heavily inspired by [ipyfilechooser](https://github.com/crahan/ipyfilechooser), released under the [MIT license](https://github.com/crahan/ipyfilechooser/blob/master/LICENSE).

Installation
------------

To install use pip:

    $ pip install ipypathchooser
    $ jupyter nbextension enable --py --sys-prefix ipypathchooser

To install for jupyterlab

    $ jupyter labextension install ipypathchooser

For a development installation (requires npm),

    $ git clone https://github.com/tslaton/ipypathchooser.git
    $ cd ipypathchooser
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix ipypathchooser
    $ jupyter nbextension enable --py --sys-prefix ipypathchooser
    $ jupyter labextension install js

When actively developing your extension, build Jupyter Lab with the command:

    $ jupyter lab --watch

This take a minute or so to get started, but then allows you to hot-reload your javascript extension.
To see a change, save your javascript, watch the terminal for an update.

Note on first `jupyter lab --watch`, you may need to touch a file to get Jupyter Lab to open.

