""" This will show detailed information about an item """

try:
    from PySide2 import QtWidgets, QtCore
except:
    from PyQt5 import QtWidgets, QtCore

from os import path, system, remove, listdir
from os.path import isfile, join
import model
# from os import listdir, system, path, remove, rename
from functools import partial
import info_view


class CollectionView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        """Initializes the Qt Widgets and class variables."""
        super(CollectionView, self).__init__(parent)

        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)

        self.icons_table_widget = QtWidgets.QTableWidget()
        self.icons_table_widget.cellClicked.connect(self.display_file_info)
        self.icons_table_widget.cellDoubleClicked.connect(self.open_item)

        self.icon_image_path = "/images/folder_icon.png"
        self.NUMBER_OF_GRID_COLUMNS = 1
        self.data = None
        self.item_paths = []

        self.info_obj = info_view.InfoView()

        layout.addWidget(self.icons_table_widget)
        layout.addWidget(self.info_obj)

    def populate(self, data):
        """ Populates the Collection View area of the app.
        :param data: object that contains the full path of the folder(or file), the list of files it contains, and some
                     methods to help process the data.
        :type data: object of file.FileItem  """
        self.data = data
        meta = data.get_info()
        if 'full_path' not in meta:
            print("Could not find file path in dictionary")
            return
        item_path = meta['full_path']

        # Clear Icons View:
        self.icons_table_widget.clearContents()
        self.item_paths = []

        if 'type' not in meta:
            print("Could not find item type (file or folder) in dictionary.")
            return

        # File:
        if meta['type'] == 'File':  # If we remove files from the collection view, we can delete this check.
            return

        # Directory:
        list_of_files = []
        list_of_folders = []
        list_of_files_and_folders = listdir(item_path)
        for item in list_of_files_and_folders:
            if path.isfile(path.join(item_path, item)):  # Request addition of 'file_name' to data model.
                list_of_files.append(item)
            else:
                list_of_folders.append(item)

        self.icons_table_widget.setRowCount(0)
        self.icons_table_widget.setColumnCount(0)
        self.icons_table_widget.insertColumn(0)
        self.icons_table_widget.horizontalHeader().setVisible(False)

        for item in list_of_files_and_folders:
            # insert a row
            row_pos = self.icons_table_widget.rowCount()
            self.icons_table_widget.insertRow(row_pos)

            self.add_item_to_iconview(item, item_path)
            self.item_paths.append(item_path + "\\" + item)

    def display_file_info(self, clicked_row):      # Todo: Does not work if there are any spaces in the file name
        """If user single clicks on a file, creates an object of InfoView which displays details about the file.
        contents of the folder that is clicked on.
        :param clicked_row: row index of the cell that the user clicks on
        :type clicked_row: int"""
        file_path = self.item_paths[clicked_row]

        if isfile(file_path):
            self.info_obj.display_info(file_path)
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

    def open_item(self, clicked_row):
        """ If user double-clicks on a file, opens it.
        :param clicked_row: row index of the cell in the table widget that the user clicks on
        :type clicked_row: int
        """
        file_path = self.item_paths[clicked_row]
        # file_path = self.buttons_dictionary[button]
        if path.exists(file_path):
            print("Opening", file_path + "...")
            if " " in file_path:
                print("Cannot process file names with spaces, yet.")
                return
            if path.isfile(file_path):
                system("start " + file_path)
            else:
                # if it's a folder, clear both pages, and populate with data inside that folder
                # clear_grid_layout(self.icons_layout)
                self.icons_table_widget.clearContents()
                file_item_object = model.file.FileItem(
                    file_path)  # to generate data, create object of model.file FileItem
                self.populate(file_item_object)

    def add_item_to_iconview(self, file, file_path):
        """Creates a TableCellWidget widget. The widget's layout contains an icon and a text(file name).
        Adds this widget to the next row in icons_table_widget.
        :param file: file name including extension.
        :type file: str
        :param file_path: full path to the file
        :type file_path: str """

        file_name = file.split('.')[0]                                                          # removes the extension.

        if "." not in file_path:                   # Todo: use a different method. What if the file name contains a dot?
            full_path = join(file_path, file)
        else:
            full_path = file_path

        cell_widget = TableCellWidget()
        cell_widget.create_widget(file_name, full_path)

        self.icons_table_widget.setCellWidget(self.icons_table_widget.rowCount()-1, 0, cell_widget)
        self.set_table_style()

    def set_table_style(self):
        """Sets the style of the icons_table_widget QtTableWidget"""
        self.icons_table_widget.setColumnWidth(0, 200)
        self.icons_table_widget.verticalHeader().setVisible(False)
        self.icons_table_widget.setShowGrid(False)

# def set_button_style(button):
#     """ Sets the button style and dimensions. No background or border by default. Turns blue with a border on hover.
#     :param button: the buttons with the file name and icon on them.
#     :type button: QWidgets.QPushButton """
#     button.setFixedSize(250, 25)
#     button.setStyleSheet(""" QPushButton {text-align:left; background-color: none; border: none; }
#                              QPushButton:hover { background-color: #CBE1F5 }
#                              QPushButton:pressed {  border-width: 5px; background-color: #B7D9F9 } """)


class TableCellWidget(QtWidgets.QWidget):
    """Class to create a layout with a label and an icon. Useful for creating file buttons in a QTableWidget
    for a file browser."""
    def __init__(self, parent=None):
        super(TableCellWidget, self).__init__(parent)

        self.layout = QtWidgets.QHBoxLayout()

        # adjust spacings between the icon and the text
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.icon_label = QtWidgets.QLabel()
        self.text_label = QtWidgets.QLabel()
        self.layout.setAlignment(QtCore.Qt.AlignLeft)
        self.setLayout(self.layout)

    def create_widget(self, file_name, file_path):
        """Creates the TableCellWidget widget for the given file name and path.
        param file_name: name of the file to be displayed
        type file_name: str
        param file_path: path to the file
        type file_path: str"""
        self.create_icon(file_path)
        self.layout.addWidget(self.icon_label)
        self.text_label.setText(file_name)
        self.layout.addWidget(self.text_label)

    def create_icon(self, file_path):
        """ Creates icon based on the default icon for the OS.
        :param file_path: full path to the file whose icon is to be added to the button
        :type file_path: str"""
        file_info = QtCore.QFileInfo(file_path)
        icon_provider = QtWidgets.QFileIconProvider()
        icon = icon_provider.icon(file_info)
        pic = icon.pixmap(10, 10)
        self.icon_label.setPixmap(pic)




