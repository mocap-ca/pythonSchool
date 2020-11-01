""" This will show detailed information about an item.
Assumptions made: file and folder names doe not contain spaces or dots. Only one dot, before extension."""

"""Todo:
1. Files should open only on double click.
2. Allow selection of multiple items.
3. Layout width is fixed to make it uniform. Make it scalable.
4. Allow folders and files with spaces in the name
5. Allow folders and files with dots in the name? Not sure. Maybe.
6. Add a small line between the header cells in the details table, so that the user can widen the columns if needed.
7. Remove bold font for selected column in header
8. Create buttons only for the selected View type, and not for all views.
9. Request more data from model. Refer to inline comments.
10. Add LMB click options.
"""

try:
    from PySide2 import QtWidgets, QtCore
    create_signal = QtCore.Signal
except:
    from PyQt5 import QtWidgets, QtCore
    create_signal = QtCore.pyqtSignal

import datetime
from os import listdir, system, path, stat
from os.path import isfile, join
from functools import partial
import model.file


class InfoView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        """Initializes all necessary Qt widgets and variables."""
        super(InfoView, self).__init__(parent)

        self.icon_image_path = "/images/folder_icon.png"

        layout = QtWidgets.QVBoxLayout()

        self.icons_widget = QtWidgets.QWidget()
        self.icons_layout = QtWidgets.QGridLayout()

        self.details_widget = QtWidgets.QTableWidget()

        self.list_view_button = QtWidgets.QPushButton("Details View")
        self.icons_view_button = QtWidgets.QPushButton("Icons View")
        self.top_bar_layout = QtWidgets.QHBoxLayout()
        self.top_bar_layout.addWidget(self.list_view_button)
        self.top_bar_layout.addWidget(self.icons_view_button)

        self.list_view_button.clicked.connect(partial(self.switch_page, self.details_widget))
        self.icons_view_button.clicked.connect(partial(self.switch_page, self.icons_widget))

        self.stacked_pages = QtWidgets.QStackedWidget()
        self.stacked_pages.addWidget(self.details_widget)
        self.stacked_pages.addWidget(self.icons_widget)

        self.stacked_pages.setCurrentWidget(self.icons_widget)

        layout.addSpacing(1)
        layout.addLayout(self.top_bar_layout)
        layout.addWidget(self.stacked_pages)
        layout.addSpacing(1)

        self.icons_column_index = 0
        self.icons_row_index = 0
        self.NUMBER_OF_GRID_COLUMNS = 2

        self.details_header_list = ["Name", "Date", "Type", "Size"]                        # Is this a string constant??
        self.details_row_index = 0
        self.details_column_index = 0
        self.data = {}
        self.icons_filename_buttons = {}
        self.details_filename_buttons = {}

        self.setLayout(layout)
        self.setMinimumWidth(520)

    def populate(self, data):
        """Populates the Display area of the window with a stacked widget. The stacked widgets contains two pages:
        the Icons View page which shows the contents of the folder as a grid of buttons, and
        the Details View page which shows a table of files(buttons) and their details, eg., file size, date modified.
        Todo: Get file details from meta
        :param data: object that contains the full path of the folder(or file), the list of files it contains, and some
                     methods to help process the data.
        :type data: object of file.FileItem  """
        self.data = data
        meta = data.get_info()
        print("Meta: ", meta)
        if 'full_path' in meta:
            item_path = meta['full_path']
        else:
            print("Could not find file path in dictionary")
            return

        # Clear List View:
        clear_table_widget(self.details_widget)

        # Clear Icons View:
        clear_grid_layout(self.icons_layout)
        self.reset_row_column_counts()

        if 'type' in meta:
            # File:
            if meta['type'] == 'File':          # If we remove files from the collection view, we can delete this check.
                pass

            # Directory:
            elif meta['type'] == 'Dir':
                self.icons_layout.setAlignment(QtCore.Qt.AlignTop)
                files = []
                directories = []
                files_and_folders = listdir(item_path)
                print(files_and_folders)
                for item in files_and_folders:
                    if isfile(join(item_path, item)):                   # Request addition of 'file_name' to data model.
                        files.append(item)
                    else:
                        directories.append(item)

                self.reset_row_column_counts()

                self.icons_widget.setLayout(self.icons_layout)
                self.icons_layout.setSpacing(0)                       # sets spacing between widgets in the layout to 0.

                for item in files_and_folders:
                    self.add_item_to_detailsview(item, item_path)
                    self.add_item_to_iconview(item, item_path)

        else:
            print("Could not find file type in dictionary")

    def reset_row_column_counts(self):
        """ Resets the row and column indices to zero."""
        self.details_row_index = 0
        self.details_column_index = 0
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

    def add_item_to_detailsview(self, file_name, folder_path):
        """ Populates the details table widget with data.
        If it is the first time it is being called, sets up the headers.
        :param file_name: name of the file to be added to the button
        :type file_name: str
        :param folder_path: location of the folder that contains the file
        :type folder_path: str
        """

        if self.details_row_index == 0:
            create_table_widget_header(self.details_widget, self.details_header_list)

        file_path = str(join(folder_path, file_name))
        self.details_widget.insertRow(self.details_widget.rowCount())                                     # insert a row

        item_data_object = model.file.FileItem(file_path)
        item_data = item_data_object.get_info()

        # column : filename button
        button = self.create_details_filename_buttons(file_name, file_path)
        self.details_widget.setCellWidget(self.details_widget.rowCount()-1, 0, button)

        # column : date and time created
        if 'created' in item_data:
            date_created = datetime.datetime.fromtimestamp(float(item_data['created'])).strftime('%d/%m/%Y %H:%M')
            # request this from data model in required format
            self.details_widget.setItem(self.details_widget.rowCount()-1, 1,
                                        QtWidgets.QTableWidgetItem(date_created))

        # column : file type
        if 'type' in item_data:
            if item_data['type'] == 'File':
                file_type = path.splitext(file_path)[1].strip('.').upper() + " File"      # request this from data model
            else:
                file_type = "Folder"
            self.details_widget.setItem(self.details_widget.rowCount() - 1, 2, QtWidgets.QTableWidgetItem(file_type))

        # column : size
        if 'file_size' in item_data:
            file_size = convert_filesize_to_str(item_data['file_size'])       # request this for folders from data model
            self.details_widget.setItem(self.details_widget.rowCount() - 1, 3, QtWidgets.QTableWidgetItem(file_size))

        self.details_widget.setRowHeight(self.details_widget.rowCount() - 1, 25)
        add_icon_to_button(button, file_path)
        self.details_row_index += 1

        self.details_table_style()

    def on_item_clicked(self, file_path):      # Todo: Does not work if there are any spaces in the file name
        """If user clicks on a file, opens it. If user clicks on a folder, clears the display and repopulates it with
        contents of the folder that is clicked on.
        :param file_path: full path to the file or folder button that is clicked on.
        :type file_path: str"""

        print("Opening", file_path + "...")
        if " " in file_path:
            print("Cannot process file names with spaces, yet.")
            return
        if isfile(file_path):
            system("start " + file_path)
        else:
            # if it's a folder, clear both pages, and populate with data inside that folder
            clear_table_widget(self.details_widget)
            clear_grid_layout(self.icons_layout)
            file_item_object = model.file.FileItem(file_path)  # to generate data, create object of model.file FileItem
            self.populate(file_item_object)

    def increment_grid_position(self):
        """Once a grid position is filled, this method is called, to point to the next position."""
        self.icons_column_index += 1
        if self.icons_column_index == self.NUMBER_OF_GRID_COLUMNS:  # go to next row
            self.icons_row_index += 1
            self.icons_column_index = 0

    def switch_page(self, selected_widget):
        """Switches current widget in the stack over to the selected widget.
        This method has been created in case I need to change the functionality such that the buttons for a view are
        created if, and only when, that view is selected.
        :param selected_widget: The widget from the stack that needs to be set as the current widget.
        :type selected_widget: QtWidget """
        self.stacked_pages.setCurrentWidget(selected_widget)

    def details_table_style(self):
        """Sets the style for the details table widget."""

        self.details_widget.setShowGrid(False)
        self.details_widget.verticalHeader().setVisible(False)
        self.details_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # Todo: Make filenames editable
        self.details_widget.resizeColumnsToContents()
        self.details_widget.setStyleSheet("QTableWidget {background-color: transparent; border: none}"
                                          "QHeaderView::section {background-color: transparent;"
                                          "border-right:1px solid gray;}"
                                          "QHeaderView {background-color: transparent;"
                                          "border-right: 1px solid gray;}"
                                          "QTableCornerButton::section {background-color: transparent;}")
        self.details_widget.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)         # left align header text

    def create_details_filename_buttons(self, button_name, file_path):
        """ Creates a button, and makes signal-slot connections for it.
        :param button_name: name of the button.
        :type button_name: str
        :param file_path: full path to the file that is to be listed on the button.
        :type file_path: str
        :return button: button with the file name on it.
        :rtype button: QPushButton widget
        """
        button = QtWidgets.QPushButton(button_name)
        button.clicked.connect(partial(self.on_item_clicked, file_path))
        set_button_style(button)
        return button


def create_table_widget_header(widget, header_items):
    """ Creates the header for a table widget.
     :param widget: the widget for which the header needs to be added.
     :type widget: QTableWidget
     :param header_items: List of headings for the table's columns
     :rtype header_items: list of strings
     """
    widget.setRowCount(0)
    widget.setColumnCount(len(header_items))
    widget.setHorizontalHeaderLabels(header_items)


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


def clear_table_widget(table):
    """ Clears the contents of the table. Keeps the headers intact.
    :param table: table widget that needs to be cleared.
    :type table: QtWidgets.QTableWidget
    """
    table.clearContents()


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


def convert_filesize_to_str(size_long):
    """ Converts the file size from Bytes to KB, MB or GB.
    :param size_long: file size in long float
    :type size_long: long integer
    :return string value: depending on what range the input fits in, returns the value in Kilo, Mega or Giga Bytes.
    :rtype string value: str """

    if size_long < 1000:
        return str(size_long) + " B"
    elif size_long < 10 ** 6:
        return str(size_long / (10 ** 3)) + " KB"
    elif size_long < 10 ** 9:
        return str(size_long / (10 ** 6)) + " MB"
    else:
        return str(size_long / (10 ** 9)) + " GB"

















