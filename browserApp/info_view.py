""" This will show detailed information about an item.
Assumptions made: file and folder names doe not contain spaces or dots. Only one dot, before extension."""

"""Todo:
1. Files should open only on double click.
2. Allow selection of multiple items.
3. Layout width is fixed to make it uniform. Make it scalable.
4. Allow folders and files with spaces in the name
5. Allow folders and files with dots in the name? Not sure. Maybe.
6. Add a separator in-between the header cells in the details table, so that the user can widen the columns if needed.
7. Remove bold font for selected column in header
8. Create buttons only for the selected View type, and not for all views.
9. Request more data from model. Refer to inline comments.
10. Add LMB click options.
"""

from os import path
import model.file

try:
    from PySide2 import QtWidgets, QtCore, QtGui

    create_signal = QtCore.Signal
except:
    from PyQt5 import QtWidgets, QtCore, QtGui

    create_signal = QtCore.pyqtSignal


class InfoView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        """Initializes all necessary Qt widgets and variables."""
        super(InfoView, self).__init__(parent)

        layout = QtWidgets.QVBoxLayout()

        self.details_widget = QtWidgets.QTableWidget()

        layout.addSpacing(1)
        layout.addWidget(self.details_widget)
        layout.addSpacing(1)

        self.file_path = ""
        self.data = None

        self.details_header_list = ["Name", "Created", "Modified", "Type", "Size"]  # Is this a string constant list??
        self.details_row_index = 0
        self.details_column_index = 0

        self.setLayout(layout)
        self.setMinimumWidth(200)

    def display_info(self, file_path):
        """ Populates the Display area of the window with a stacked widget. The stacked widgets contains two pages:
                the Icons View page which shows the contents of the folder as a grid of buttons, and
                the Details View page which shows a table of files(buttons) and their details, eg., file size, date modified.
                Todo: Get file details from meta
                :param file_path: full path of the file
                :type file_path: str  """
        clear_table_widget(self.details_widget)

        self.file_path = file_path
        self.populate_info_table(file_path)
        self.reset_row_column_counts()

    def reset_row_column_counts(self):
        """ Resets the row and column indices to zero. """
        self.details_row_index = 1
        self.details_column_index = 1
        self.details_widget.rowCount = 1
        # print("indexes", self.details_row_index, self.details_column_index)

    def populate_info_table(self, file_path):
        """ Populates the details table widget with data.
        If it is the first time it is being called, sets up the headers.
        :param file_path: path of the file to be added to the button
        :type file_path: str
        """
        if self.details_row_index == 0:
            create_table_widget_header(self.details_widget, self.details_header_list)

        item_data_object = model.file.FileItem(file_path)
        item_data = item_data_object.get_info()
        self.details_column_index += 1

        # column : filename
        file_name = path.split(file_path)[1]
        # self.file_name_label.setText(file_name)
        self.details_widget.setItem(0, 1, QtWidgets.QTableWidgetItem(file_name))
        file_item_object = model.file.FileItem(file_path)  # to access details, create object of model.file FileItem
        item_data = file_item_object.get_info()  # get the data dictionary and store in item_data

        # column : date and time created
        if 'created' in item_data:
            date_created = item_data['created']
            self.details_widget.setItem(1, 1, QtWidgets.QTableWidgetItem(date_created))

        if 'modified' in item_data:
            date_modified = item_data['modified']
            self.details_widget.setItem(2, 1, QtWidgets.QTableWidgetItem(date_modified))

        # column : file type
        file_type = None
        if 'file_type' in item_data:
            file_type = item_data['file_type']
        elif file_name:
            file_type = file_name.split('.')[-1].upper()
        if file_type:
            self.details_widget.setItem(3, 1, QtWidgets.QTableWidgetItem(file_type))

        # column : size
        if 'file_size' in item_data:
            file_size = item_data['file_size']  # request this for folders from data model
            if type(file_size) is float:
                file_size = convert_filesize_to_str(file_size)

            self.details_widget.setItem(4, 1, QtWidgets.QTableWidgetItem(file_size))

        self.details_table_style()

    def details_table_style(self):
        """Sets the style for the details table widget."""

        self.details_widget.setShowGrid(False)
        self.details_widget.horizontalHeader().setVisible(False)
        self.details_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # Todo: Make filenames editable
        self.details_widget.resizeColumnsToContents()
        self.details_widget.setStyleSheet("QTableWidget {background-color: transparent; border: none}"
                                          "QHeaderView::section {background-color: transparent;"
                                          "border-right:1px solid gray;}"
                                          "QHeaderView {background-color: transparent;"
                                          "border-right: 1px solid gray;}"
                                          "QTableCornerButton::section {background-color: transparent;}")
        self.details_widget.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)  # left align header text

    def clear_grid_layout(grid_layout):
        """ Deletes all the contents of a grid layout.
        :param grid_layout: The layout the needs to be cleared.
        :type grid_layout: QtWidgets.QGridLayout """

        # clear all icons_filename_buttons
        while grid_layout.count():
            child = grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


def create_table_widget_header(widget, header_items):
    """ Creates the header for a table widget.
     :param widget: the widget for which the header needs to be added.
     :type widget: QTableWidget
     :param header_items: List of headings for the table's columns
     :rtype header_items: list of strings
     """
    widget.setColumnCount(2)  # ?? Re-think this.
    widget.setRowCount(len(header_items))
    widget.setVerticalHeaderLabels(header_items)


def clear_table_widget(table):
    """ Clears the contents of the table. Keeps the headers intact.
    :param table: table widget that needs to be cleared.
    :type table: QtWidgets.QTableWidget
    """
    table.clearContents()


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
