""" This will show detailed information about an item """

try:
    from PySide2 import QtWidgets, QtCore
except:
    from PyQt5 import QtWidgets, QtCore

from os import path, system, remove, listdir
from os.path import isfile, join
import model
from functools import partial
import info_view


class CollectionView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CollectionView, self).__init__(parent)

        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)

        self.icons_widget = QtWidgets.QWidget()
        self.icons_layout = QtWidgets.QGridLayout()
        self.icon_image_path = "/images/folder_icon.png"
        self.icons_column_index = 0
        self.icons_row_index = 0
        self.NUMBER_OF_GRID_COLUMNS = 1
        self.data = None

        self.info = info_view.InfoView()

        layout.addWidget(self.icons_widget)
        layout.addWidget(self.info)
        # self.icons_filename_buttons = {}

    def populate(self, data):
        """ Populates the Display area of the window with a stacked widget. The stacked widgets contains two pages:
                the Icons View page which shows the contents of the folder as a grid of buttons, and
                the Details View page which shows a table of files(buttons) and their details, eg., file size, date modified.
                Todo: Get file details from meta
                :param data: object that contains the full path of the folder(or file), the list of files it contains, and some
                             methods to help process the data.
                :type data: object of file.FileItem  """
        self.data = data
        meta = data.get_info()
        print("Meta: ", meta)
        if 'full_path' not in meta:
            print("Could not find file path in dictionary")
            return
        item_path = meta['full_path']

        # Clear Icons View:
        clear_grid_layout(self.icons_layout)
        self.reset_row_column_counts()
        # self.add_view_options_buttons(self.icons_layout)

        if 'type' not in meta:
            print("Could not find item type (file or folder) in dictionary.")
            return

        # File:
        if meta['type'] == 'File':  # If we remove files from the collection view, we can delete this check.
            return

        # Directory:
        self.icons_layout.setAlignment(QtCore.Qt.AlignTop)
        list_of_files = []
        list_of_folders = []
        list_of_files_and_folders = listdir(item_path)
        print(list_of_files_and_folders)
        for item in list_of_files_and_folders:
            if path.isfile(path.join(item_path, item)):  # Request addition of 'file_name' to data model.
                list_of_files.append(item)
            else:
                list_of_folders.append(item)

        self.reset_row_column_counts()

        self.icons_widget.setLayout(self.icons_layout)
        self.icons_layout.setSpacing(0)  # sets spacing between widgets in the layout to 0.

        for item in list_of_files_and_folders:
            self.add_item_to_iconview(item, item_path)

    def on_item_clicked(self, file_path):      # Todo: Does not work if there are any spaces in the file name
        """If user clicks on a file, opens it. If user clicks on a folder, clears the display and repopulates it with
        contents of the folder that is clicked on.
        :param file_path: full path to the file or folder button that is clicked on.
        :type file_path: str"""
        if isfile(file_path):
            self.info.display_info(file_path)
        else:
            print("Not handled folders yet. App is still under construction.")

    def show_rightclick_menu(self, button, point):
        """ Displays a menu on right mouse button click.
        :param button: button user clicks on.
        :type button: QPushButton
        :param point: ??
        :type point: QtCore.QPoint
        """

        # create context menu
        pop_menu = QtWidgets.QMenu(self)

        delete_action = QtWidgets.QAction('Delete', self)
        pop_menu.addAction(delete_action)
        delete_action.triggered.connect(partial(self.delete_item, button))

        open_action = QtWidgets.QAction('Open', self)
        pop_menu.addAction(open_action)
        open_action.triggered.connect(partial(self.open_item, button))

        # rename_action = QtWidgets.QAction('Rename', self)
        # pop_menu.addAction(rename_action)
        # rename_action.triggered.connect(partial(self.rename_item, button))

        # show context menu
        pop_menu.exec_(button.mapToGlobal(point))

    def delete_item(self, button):
        """ Deletes the selected file.
        :param button: button user clicks on.
        :type button: QPushButton
        """
        if path.exists(self.buttons_dictionary[button]):
            remove(self.buttons_dictionary[button])
        print("Deleted:", self.buttons_dictionary[button])

        # refresh view
        self.refresh_details_view()

    def refresh_details_view(self):
        """ Refreshes the view. """
        pass                                                                                       # Todo

    def open_item(self, button):
        """ Opens the selected file.
        :param button: button user clicks on.
        :type button: QPushButton
        """
        file_path = self.buttons_dictionary[button]
        if path.exists(file_path):
            print("Opening", file_path + "...")
            if " " in file_path:
                print("Cannot process file names with spaces, yet.")
                return
            if path.isfile(file_path):
                system("start " + file_path)
            else:
                # if it's a folder, clear both pages, and populate with data inside that folder
                clear_grid_layout(self.icons_layout)
                file_item_object = model.file.FileItem(
                    file_path)  # to generate data, create object of model.file FileItem
                self.populate(file_item_object)

    def increment_grid_position(self):
        """Once a grid position is filled, this method is called, to point to the next position."""
        self.icons_column_index += 1
        if self.icons_column_index == self.NUMBER_OF_GRID_COLUMNS:  # go to next row
            self.icons_row_index += 1
            self.icons_column_index = 0

    def reset_row_column_counts(self):
        self.icons_column_index = 0
        self.icons_row_index = 0

    def add_item_to_iconview(self, file, file_path):
        """Creates a button, sets its style, and adds it to the Icons View page. Makes signal-slot connections.
        The button displays an icon and the file name.
        :param file: file name including extension.
        :type file: str
        :param file_path: full path to the file
        :type file_path: str """

        file_name = file.split('.')[0]                                                          # removes the extension.
        button = QtWidgets.QPushButton(file_name)
        set_button_style(button)

        if "." not in file_path:                   # Todo: use a different method. What if the file name contains a dot?
            full_path = join(file_path, file)
        else:
            full_path = file_path
        add_icon_to_button(button, full_path)
        button.clicked.connect(partial(self.on_item_clicked, full_path))

        self.icons_layout.addWidget(button, self.icons_row_index, self.icons_column_index)
        self.increment_grid_position()


def clear_grid_layout(grid_layout):
    """ Deletes all the contents of a grid layout.
    :param grid_layout: The layout the needs to be cleared.
    :type grid_layout: QtWidgets.QGridLayout """

    # clear all icons_filename_buttons
    while grid_layout.count():
        child = grid_layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()


def set_button_style(button):
    """ Sets the button style and dimensions. No background or border by default. Turns blue with a border on hover.
    :param button: the buttons with the file name and icon on them.
    :type button: QWidgets.QPushButton """
    button.setFixedSize(250, 25)
    button.setStyleSheet(""" QPushButton {text-align:left; background-color: none; border: none; }
                             QPushButton:hover { background-color: #CBE1F5 }
                             QPushButton:pressed {  border-width: 5px; background-color: #B7D9F9 } """)


def add_icon_to_button(button, file_path):
    """Adds an icon to the button that is the windows standard icon associated with that file.
    :param button: button to which the icon is to be added
    :type button: QPushButton
    :param file_path: full path to the file whose icon is to be added to the button
    :type file_path: str"""
    file_info = QtCore.QFileInfo(file_path)
    icon_provider = QtWidgets.QFileIconProvider()
    icon = icon_provider.icon(file_info)
    button.setIcon(icon)







        # self.label.clear()
        # for label in self.labels:
        #     label.clear()
        #     self.layout().removeWidget(label)
        # # self.labels.clear()
        #
        # child_count = items.children()
        # if child_count == 0:
        #     return
        #
        # file_size = 0
        #
        # for i in range(child_count):
        #     subitem = items.get_child(i)
        #     meta = subitem.get_info()
        #
        #     if "file_size" in meta:
        #         file_size += meta["file_size"]
        #
        # self.label.setText("Total Size: %d" % file_size)
        #
        # keys = set()
        # integer_values = {}
        #
        # # Get keys
        # for i in range(child_count):
        #     subitem = items.get_child(i)
        #     meta = subitem.get_info()
        #     keys.update(meta.keys())
        #
        # # Get cumulative key values
        # for i in range(child_count):
        #     subitem = items.get_child(i)
        #     meta = subitem.get_info()
        #
        #     for key in [x for x in keys if x in meta]:
        #         value = meta[key]
        #         if isinstance(value, int):
        #             if key not in integer_values:
        #                 integer_values[key] = 0
        #             integer_values[key] += value
        #
        #
        # print(integer_values)






