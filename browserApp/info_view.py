""" This will show detailed information about an item.
Assumptions made: file and folder names doe not contain spaces or dots. Only one dot, before extension."""


try:
    from PySide2 import QtWidgets, QtCore
    create_signal = QtCore.Signal
except:
    from PyQt5 import QtWidgets, QtCore
    create_signal = QtCore.pyqtSignal

import time
from os import listdir, system, path, stat
from os.path import isfile, join
from functools import partial


class InfoView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(InfoView, self).__init__(parent)

        self.icon_image_path = "/images/folder_icon.png"

        layout = QtWidgets.QVBoxLayout()

        self.icons_widget = QtWidgets.QWidget()
        self.icons_layout = QtWidgets.QGridLayout()
        self.buttons_dict = {}

        self.details_widget = QtWidgets.QTableWidget()

        self.list_view_button = QtWidgets.QPushButton("Details View")
        self.icons_view_button = QtWidgets.QPushButton("Icons View")
        self.top_bar_layout = QtWidgets.QHBoxLayout()
        self.top_bar_layout.addWidget(self.list_view_button)
        self.top_bar_layout.addWidget(self.icons_view_button)

        self.list_view_button.clicked.connect(self.setup_list_view)
        self.icons_view_button.clicked.connect(self.setup_icons_view)

        self.stacked_pages = QtWidgets.QStackedWidget()
        self.stacked_pages.addWidget(self.details_widget)
        self.stacked_pages.addWidget(self.icons_widget)

        self.stacked_pages.setCurrentWidget(self.icons_widget)

        layout.addSpacing(1)
        layout.addLayout(self.top_bar_layout)
        layout.addWidget(self.stacked_pages)
        layout.addSpacing(1)

        self.details_header_list = ["Name", "Date", "Type", "Size"]
        self.icons_column_index = 0
        self.icons_row_index = 0
        self.details_row_index = 0
        self.details_column_index = 0
        self.data = {}
        self.icons_filename_buttons = {}
        self.details_filename_buttons = {}

        self.setLayout(layout)
        self.setMinimumWidth(520)

    def populate(self, data):
        self.data = data

        meta = data.get_info()
        print("Meta: ", meta)
        if 'full_path' in meta:
            item_path = meta['full_path']
        else:
            print("Could not find file path in dictionary")
            return

        # Clear List View:
        self.clear_details_widget(self.details_widget)

        # Clear Icons View:
        self.clear_icons_layout(self.icons_layout)

        if 'type' in meta:
            # File:
            if meta['type'] == 'File':          # If we remove files from the collection view, we can delete this check.
                pass
                # self.process_details_view(item_path, item_path)
                # self.process_icons_view(item_path, item_path)
                #
                # self.clear_icons_layout(self.icons_layout)
                # self.icons_layout.setAlignment(QtCore.Qt.AlignTop)

            # Directory:
            elif meta['type'] == 'Dir':

                self.icons_layout.setAlignment(QtCore.Qt.AlignTop)
                files = []
                directories = []
                # Request addition of 'file_name' to data model
                files_and_folders = listdir(item_path)
                for item in files_and_folders:
                    if isfile(join(item_path, item)):
                        files.append(item)
                    else:
                        directories.append(item)

                print("Files: ", files, "Folders:", directories)

                # process files
                self.reset_row_column_counts()
                # for file in files:
                #     print("file: ", file)
                #     self.process_details_view(file, item_path)
                #     self.process_icons_view(file, item_path)

                for item in files_and_folders:
                    self.process_details_view(item, item_path)
                    self.process_icons_view(item, item_path)

        else:
            print("Could not find file type in dictionary")

    def reset_row_column_counts(self):
        self.details_row_index = 0
        self.details_column_index = 0
        self.icons_column_index = 0
        self.icons_row_index = 0

    def process_icons_view(self, file, file_path):
        self.icons_widget.setLayout(self.icons_layout)
        self.icons_layout.setSpacing(0)
        file_name = file.split('.')[0]
        button = QtWidgets.QPushButton(file_name)

        self.buttons_dict[file_name] = button

        self.icons_layout.addWidget(button, self.icons_row_index, self.icons_column_index)
        self.update_grid_positions()
        self.set_button_style(button)

        if "." not in file_path:
            full_path = join(file_path, file)
        else:
            full_path = file_path

        # signal-slot connection for file icons_filename_buttons:
        button.clicked.connect(partial(self.on_item_clicked, file, full_path))

        self.add_icon_to_button(button, full_path)

    def add_icon_to_button(self, button, file_path):
        file_info = QtCore.QFileInfo(str(file_path))
        icon_provider = QtWidgets.QFileIconProvider()
        icon = icon_provider.icon(file_info)
        button.setIcon(icon)

    def on_item_clicked(self, file_name, file_path):                    # ?? Does not work if there are any spaces in the file name
        print("Opening", file_path, "...")
        if " " in file_path:
            print("Cannot process file names with spaces, yet.")
            return
        if isfile(file_name):
            system("start " + file_path)
        else:
            print("found directory", file_name)


    def size_in_str(self, size_float):
        if size_float < 1000:
            return str(size_float) + " B"
        elif size_float < 10 ** 6:
            return str(size_float / (10 ** 3)) + " KB"
        elif size_float < 10 ** 9:
            return str(size_float/(10 ** 6)) + " MB"
        else:
            return str(size_float/(10 ** 9)) + " GB"

    def clear_details_widget(self, table):
        table.clearContents()

    def clear_icons_layout(self, icons_layout):
        # clear all icons_filename_buttons
        while icons_layout.count():
            child = icons_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        # file icons_filename_buttons
        self.icons_column_index = 0
        self.icons_row_index = 0

    def update_grid_positions(self):
        self.icons_column_index += 1
        if self.icons_column_index == 2:  # go to next row
            self.icons_row_index += 1
            self.icons_column_index = 0

    def set_button_style(self, button):
        button.setFixedSize(250, 25)
        # button.setIcon(QtGui.QIcon(icon_path))
        button.setStyleSheet("""QPushButton {text-align:left; background-color: none; border: none; }
        QPushButton:hover { background-color: #CBE1F5 }
        QPushButton:pressed {  border-width: 5px; background-color: #B7D9F9 }""")


    def setup_list_view(self):
        self.stacked_pages.setCurrentWidget(self.details_widget)


    def setup_icons_view(self):
        self.stacked_pages.setCurrentWidget(self.icons_widget)

    def process_details_view(self, file_name, file_path):
        if self.details_row_index == 0:
            self.details_widget.setRowCount(self.details_row_index)
            self.details_widget.setColumnCount(len(self.details_header_list))
            self.details_widget.setHorizontalHeaderLabels(self.details_header_list)

        full_path = file_path + "\\" + file_name
        self.details_widget.insertRow(self.details_widget.rowCount())

        # column : filename button
        button = self.create_details_filename_buttons(file_name, file_name, full_path)
        self.details_widget.setCellWidget(self.details_widget.rowCount()-1, 0, button)

        # column : date and time modified
        date_modified = time.ctime(path.getmtime(full_path))                           # request this from data model
        self.details_widget.setItem(self.details_widget.rowCount()-1, 1, QtWidgets.QTableWidgetItem(str(date_modified)))

        # column : file type
        file_type = path.splitext(full_path)[1].strip('.').upper() + " File"           # request this from data model
        self.details_widget.setItem(self.details_widget.rowCount()-1, 2, QtWidgets.QTableWidgetItem(file_type))

        # column : size
        file_size = self.size_in_str(stat(full_path).st_size)                          # request this from data model
        self.details_widget.setItem(self.details_widget.rowCount() - 1, 3, QtWidgets.QTableWidgetItem(file_size))

        self.details_widget.setRowHeight(self.details_widget.rowCount() - 1, 25)
        self.add_icon_to_button(button, full_path)
        self.details_row_index += 1

        self.details_table_style()

    def details_table_style(self):
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

    def create_details_filename_buttons(self, button_name, file_name, file_path):
        button = QtWidgets.QPushButton(button_name)
        button.clicked.connect(partial(self.on_item_clicked, file_name, file_path))
        self.set_button_style(button)
        return button


















