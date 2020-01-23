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

    $ jupyter labextension install @jupyter-widgets/jupyterlab-manager
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

Usage
-----

A PathChooser can be instantiated as follows:
![](https://i.imgur.com/jcwq2ig.png)

Clicking _Choose_ will open the PathChooser:
![](https://i.imgur.com/CHp7cSv.png))

Select a file or directory with a single click or by typing its name in the text box at the top right:
![](https://i.imgur.com/QmsJEUo.png)

A selected file or directory can be chosen by clicking the _Choose_ button:
![](https://i.imgur.com/f2q0zyt.png)

The chosen path can be further modified by clicking _Change_.

To navigate into a directory, double-click it.

To navigate up a level, double-click `..` or use the path list dropdown in the top left.

If you double-click a file, it will automatically be chosen. 

To choose a directory, you must first select it and click the _Choose_ or _Change_ button.

To read out the chosen path from a PathChooser called `chooser`, you would access `chooser.chosen_path`. 

There are various options that can be set during instantiation or after the fact to customize the widget's behavior.

The constructor handles most of them and is as follows:

```{python}
class PathChooser(VBox):
    def __init__(
            self,
            default_directory=os.getcwd(),
            chosen_path_desc='',
            on_chosen_path_change=None,
            title='',
            show_hidden=False,
            **kwargs,
        ):
        """
        PathChooser constructor.

        :param default_directory: The initial directory
        :param chosen_path_desc: A label for what the chosen path represents
        :param on_chosen_path_change: A callback receiving (old_path, new_path)
        :param title: A title for the whole widget
        :param show_hidden: Show hidden files and folders
        """
```
