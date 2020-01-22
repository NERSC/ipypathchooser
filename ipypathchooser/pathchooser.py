# Standard lib
import os
# Third party
from ipywidgets import (
    Dropdown, Text, Select, Button, HTML,
    Layout, GridBox, HBox, VBox, Output
)
# Local
from . import utils
from .double_click_select import DoubleClickSelect

font_awesome_folder_unicode = '\uf07b'
nonbreaking_space = '\xa0'

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

        self._default_directory = default_directory.rstrip(os.path.sep)
        # chosen_path_desc is used directly below in an HTML widget
        self.on_chosen_path_change = on_chosen_path_change
        self._title = HTML(
            value=title,
        )
        if title is '':
            self._title.layout.display = 'none'
        self._show_hidden = show_hidden

        # For debugging
        self.output = Output(layout={'border': '1px solid white'})

        # Widgets
        # A dropdown with the current directory and its ancestors
        self._path_list = Dropdown(
            description='',
            layout=Layout(
                width='auto',
                grid_area='path-list',
            )
        )
        # A textbox for setting and describing the selected item
        self._selected_item = Text(
            placeholder='selected item',
            layout=Layout(
                width='auto',
                grid_area='selected-item',
            )
        )
        # A select listing the contents of the current directory
        self._directory_content = DoubleClickSelect(
            rows=8,
            layout=Layout(
                width='auto',
                grid_area='directory-content',
            )
        )
        self._observe_widgets()

        # The path chosen upon finalization of form values
        self._chosen_path = ''
        # A label listing the chosen path
        self._chosen_path_label = HTML(
            value=self.chosen_path,
            placeholder='',
            description=chosen_path_desc,
        )

        # A button for finalizing the current form values
        self._choose = Button(
            description='Choose',
            layout=Layout(width='auto'),
        )
        self._choose.on_click(self._on_choose_click)

        # A button for canceling pending changes to the form
        self._cancel = Button(
            description='Cancel',
            layout=Layout(
                width='auto',
                display='none',
            )
        )
        self._cancel.on_click(self._on_cancel_click)

        # Layout
        self._main_area = GridBox(
            children=[
                self._path_list,
                self._selected_item,
                self._directory_content,
            ],
            layout=Layout(
                display='none',
                width='500px',
                grid_gap='0px 0px',
                grid_template_rows='auto auto',
                grid_template_columns='60% 40%',
                grid_template_areas='''
                    'path-list selected-item'
                    'directory-content directory-content'
                    ''',
            )
        )
        self._bottom_bar = HBox(
            children=[
                self._chosen_path_label,
                self._choose,
                self._cancel,
            ],
            layout=Layout(width='auto'),
        )

        # Set initial form values
        self._set_form_values(
            self._default_directory,
        )

        # Call VBox super class __init__
        super().__init__(
            children=[
                self._title,
                self._main_area,
                self._bottom_bar,
            ],
            layout=Layout(width='auto'),
            **kwargs,
        )

    def _observe_widgets(self, active=True):
        """
        A helper function for toggling interactive element's callbacks.
        """
        widgets_vs_callbacks = [
            (self._path_list, self._on_path_list_select),
            (self._selected_item, self._on_selected_item_change),
            (self._directory_content, self._on_directory_content_select),
        ]
        if active:
            for widget, callback in widgets_vs_callbacks:
                    widget.observe(callback, names='value')
            self._directory_content.observe(
                self._on_directory_doubleclick,
                names='dblclick',
            )
        else:
            for widget, callback in widgets_vs_callbacks:
                widget.unobserve(callback, names='value')
            self._directory_content.unobserve(
                self._on_directory_doubleclick,
                names='dblclick',
            )

    def _set_form_values(self, current_directory=None, selected_item=None):
        """
        Set the two defining values of the PathChooser.

        :param current_directory: The directory the chooser is looking at
        :param selected_item: The item (file or directory) chosen within the current_directory
        """
        # Temporarily disable widget callbacks to silently manipulate values
        self._observe_widgets(False)

        if current_directory:
            self._path_list.options = utils.get_subpaths(current_directory)
            self._path_list.value = current_directory
            types_vs_contents = utils.get_dir_contents(
                current_directory,
                hidden=self._show_hidden,
            )
            self._directory_content.icons = [
                font_awesome_folder_unicode if x[0] == 'directory' else nonbreaking_space * 4
                for x in types_vs_contents
            ]
            self._directory_content.options = [x[1] for x in types_vs_contents]
        if selected_item:
            self._selected_item.value = selected_item

        # Select items entered in text box matching directory contents
        if selected_item in self._directory_content.options:
            self._directory_content.value = selected_item
        else:
            self._directory_content.value = None

        # Set the state of the Choose button when _main_area is visible
        if self._main_area.layout.display is None:
            self._choose.disabled = self._directory_content.value is None

        # Re-enable widget triggers
        self._observe_widgets()

    def _on_path_list_select(self, change):
        """
        Handler for when a new path is selected from the path list dropdown.
        """
        self._set_form_values(
            change.new,
        )

    def _on_directory_content_select(self, change):
        """
        Handler for when a directory entry is selected.
        """
        current_directory = self._path_list.value
        selected_item = change.new
        if selected_item != '..':
            self._set_form_values(
                current_directory,
                selected_item,
            )

    def _on_directory_doubleclick(self, change):
        dblclick_index = change.new
        current_directory = self._path_list.value
        clicked_item = self._directory_content.options[dblclick_index]
        # Navigate up
        if clicked_item == '..':
            self._set_form_values(os.path.dirname(current_directory))
        else:
            new_path = os.path.join(current_directory, clicked_item)
            # Navigate down
            if os.path.isdir(new_path):
                self._set_form_values(new_path)
            # Choose the file
            elif os.path.isfile(new_path):
                self.hide()
                self.chosen_path = new_path

    def _on_selected_item_change(self, change):
        """
        Handler for when the _selected_item text field changes.
        """
        self._set_form_values(selected_item=change.new)

    def show(self):
        """
        Open the PathChooser.
        """
        self._main_area.layout.display = None
        self._cancel.layout.display = None

    def hide(self):
        """
        Hide the PathChooser.
        """
        self._main_area.layout.display = 'none'
        self._cancel.layout.display = 'none'

    def _on_choose_click(self, button):
        """
        Handler for when the choose button is clicked.
        """
        # If _main_area is not visible, make it visible and show the cancel button
        if self._main_area.layout.display is 'none':
            self.show()
            self._set_form_values()
        # Otherwise, hide the _main_area and the cancel button
        else:
            self.hide()
            chosen_path = os.path.join(self._path_list.value, self._selected_item.value)
            self.chosen_path = chosen_path

    def _on_cancel_click(self, button):
        """
        Handler for when the cancel button is clicked.
        """
        self.hide()
        self._choose.disabled = False

    def reset(self):
        """
        Reset the form to its defaults.
        """
        self.chosen_path = ''
        self.set_form_values(
            self._default_directory,
            '',
        )

    def refresh(self):
        """
        Re-render the form.
        """
        self._set_form_values(
            self._path_list.value,
            self._selected_item.value,
        )

    def print(self, message):
        """
        Print `message` to self.output for debugging purposes.
        """
        self.output.append_stdout(f'{message}\n')

    @property
    def show_hidden(self):
        """
        Get the current visibility setting for hidden files and folders.
        """
        return self._show_hidden

    @show_hidden.setter
    def show_hidden(self, hidden):
        """
        Set the visibility of hidden files and folders.
        """
        self._show_hidden = hidden
        self.refresh()

    @property
    def rows(self):
        """
        Get current number of rows.
        """
        return self._dircontent.rows

    @rows.setter
    def rows(self, rows):
        """
        Set number of rows.
        """
        self._dircontent.rows = rows

    @property
    def title(self):
        """
        Get the title.
        """
        return self._title.value

    @title.setter
    def title(self, title):
        """
        Set the title.
        """
        self._title.value = title

        if title is '':
            self._title.layout.display = 'none'
        else:
            self._title.layout.display = None

    @property
    def chosen_path(self):
        """
        Get the chosen_path value.
        """
        return self._chosen_path

    @chosen_path.setter
    def chosen_path(self, chosen_path):
        """
        Set chosen_path and update chosen_path_label. Trigger callback if present.
        """
        old_path = self._chosen_path
        self._chosen_path = chosen_path
        self._choose.description = 'Change' if chosen_path else 'Choose'
        self._chosen_path_label.value = chosen_path + ('&nbsp;'*2)
        if self.on_chosen_path_change:
            self.on_chosen_path_change(old_path, chosen_path)

    def __repr__(self):
        str_ = ("PathChooser("
                "current_directory='{0}', "
                "selected_item='{1}', "
                "show_hidden='{2}')").format(
            self._path_list.value,
            self._selected_item.value,
            self._show_hidden,
        )
        return str_
