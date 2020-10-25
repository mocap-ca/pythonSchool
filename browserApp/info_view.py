""" This will show detailed information about an item """
import os

try:
    from PySide2 import QtWidgets, QtCore, QtGui
except:
    from PyQt5 import QtWidgets, QtCore, QtGui

from os import listdir, open, O_RDWR
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

        self.list_widget = QtWidgets.QWidget()
        self.list_layout = QtWidgets.QGridLayout()
        self.list_grid_column_index = 0
        self.list_grid_row_index = 1
        # self.list_widget.setLayout(self.list_layout)
        self.list_layout.setAlignment(QtCore.Qt.AlignTop)
        self.file_name_header = QtWidgets.QLabel("File:")
        self.size_header = QtWidgets.QLabel("Size:")
        self.type_header = QtWidgets.QLabel("Type:")
        self.created_header = QtWidgets.QLabel("Created:")
        self.list_layout.addWidget(self.file_name_header, 0, 0)
        self.list_layout.addWidget(self.size_header, 0, 1)
        self.list_layout.addWidget(self.type_header, 0, 2)
        self.list_layout.addWidget(self.created_header, 0, 3)

        self.list_view_button = QtWidgets.QPushButton("List View")
        self.icons_view_button = QtWidgets.QPushButton("Icon View")
        self.top_bar_layout = QtWidgets.QHBoxLayout()
        self.top_bar_layout.addWidget(self.list_view_button)
        self.top_bar_layout.addWidget(self.icons_view_button)

        self.list_view_button.clicked.connect(self.setup_list_view)
        self.icons_view_button.clicked.connect(self.setup_icons_view)

        self.stacked_pages = QtWidgets.QStackedWidget()
        self.stacked_pages.addWidget(self.list_widget)
        self.stacked_pages.addWidget(self.icons_widget)

        self.stacked_pages.setCurrentWidget(self.icons_widget)

        layout.addSpacing(1)
        layout.addLayout(self.top_bar_layout)
        layout.addWidget(self.stacked_pages)
        layout.addSpacing(1)

        self.column_index = 0
        self.row_index = 0
        self.data = {}
        self.setLayout(layout)

    def populate(self, data):
        self.data = data

        # Clear the list_table
        self.clear_layout(self.list_layout)

        # If item clicked on is a file, display info in list_table. Else, display buttons with file names.
        meta = data.get_info()
        self.list_grid_row_index += 1
        if 'full_path' in meta:
            item_path = meta['full_path']
            print("full_path is : ", item_path)
        else:
            print("Could not find file path in dictionary")
            return

        if 'type' in meta:
            # File:
            if meta['type'] == 'File':          # If we remove files from the collection view, we can delete this check.
                self.process_file(meta, item_path, item_path)

            # Directory:
            elif meta['type'] == 'Dir':
                self.clear_layout(self.icons_layout)
                self.icons_layout.setAlignment(QtCore.Qt.AlignTop)

                # Request addition of 'file_name' to data model

                files = [f for f in listdir(item_path) if isfile(join(item_path, f))]
                print(files)

                for file in files:
                    print("file: ", file)
                    self.process_file(meta, file, item_path)
        else:
            print("Could not find file type in dictionary")

    def process_file(self, meta, file, file_path):

        # LIST VIEW
        self.list_widget.setLayout(self.list_layout)
        self.list_grid_row_index += 1
        if 'file_size' in meta:
            file_size = meta['file_size']
            size_label = QtWidgets.QLabel("0.0 MB")
            self.list_grid_column_index = 1
            self.list_layout.addWidget(size_label, 1, 1)

        # ICON VIEW
        self.icons_widget.setLayout(self.icons_layout)
        self.icons_layout.setSpacing(0)
        file_name = file.split('.')[0]
        button = QtWidgets.QPushButton(file_name)

        self.buttons_dict[file_name] = button

        self.icons_layout.addWidget(button, self.row_index, self.column_index)
        self.update_grid_positions()
        self.set_button_style(button, self.icon_image_path)

        if "." not in file_path:
            path = file_path + "\\" + file
        else:
            path = file_path
        # signal-slot connection for file buttons:
        button.clicked.connect(partial(self.on_item_clicked, path))

        file_info = QtCore.QFileInfo(path)
        icon_provider = QtWidgets.QFileIconProvider()
        icon = icon_provider.icon(file_info)

        button.setIcon(icon)

    # file_name = os.path.basename(meta['full_path'])

    def on_item_clicked(self, file):   # Does not work if there are any spaces in the file name
        print(file)
        os.system("start " + file)
        if " " in file:
            print("Cannot process file names with spaces, yet.")
            return


    def clear_layout(self, icons_layout):   # request to add the method in stub
        # clear all buttons
        while self.icons_layout.count():
            child = self.icons_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        # file buttons
        self.column_index = 0
        self.row_index = 0

    def update_grid_positions(self):
        self.column_index += 1
        if self.column_index == 2:  # go to next row
            self.row_index += 1
            self.column_index = 0

    def set_button_style(self, button, icon_path):
        button.setFixedSize(250, 25)
        # button.setIcon(QtGui.QIcon(icon_path))

        button.setStyleSheet("""QPushButton {text-align:left; background-color: none; border: none; }
        QPushButton:hover { background-color: #CBE1F5 }
        QPushButton:pressed {  border-width: 5px; background-color: #B7D9F9 }""")


    def setup_list_view(self):
        self.stacked_pages.setCurrentWidget(self.list_widget)


    def setup_icons_view(self):
        self.stacked_pages.setCurrentWidget(self.icons_widget)
















