""" This will show detailed information about an item """

try:
    from PySide2 import QtWidgets, QtCore
    create_signal = QtCore.Signal
except:
    from PyQt5 import QtWidgets, QtCore
    create_signal = QtCore.pyqtSignal

from os import listdir, open, O_RDWR
from os.path import isfile, join
from functools import partial

class InfoView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(InfoView, self).__init__(parent)

        layout = QtWidgets.QVBoxLayout()

        self.icons_widget = QtWidgets.QWidget()
        self.icons_layout = QtWidgets.QGridLayout()

        self.list_table = QtWidgets.QWidget()
        self.list_layout = QtWidgets.QGridLayout()
        self.list_table.setLayout(self.list_layout)
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
        self.stacked_pages.addWidget(self.list_table)
        self.stacked_pages.addWidget(self.icons_widget)

        self.stacked_pages.setCurrentWidget(self.list_table)

        layout.addSpacing(1)
        layout.addLayout(self.top_bar_layout)
        layout.addWidget(self.stacked_pages)
        layout.addSpacing(1)

        self.column_index = 0
        self.row_index = 0

        self.buttons = {}

        self.setLayout(layout)

    def populate(self, data):
        # print("Do something useful with: " + str(data))

        # Clear the list_table
        self.clear_layout(self.list_layout)
        self.stacked_pages.setCurrentWidget(self.list_table)

        # If item clicked on is a file, display info in list_table. Else, display buttons with file names.
        meta = data.get_info()
        if 'type' in meta:
            # File:
            if meta['type'] == 'File':
                pass
                # for k, v in meta.items():
                #     item = QtWidgets.QTreeWidgetItem([k, v])
                #     self.details_list_table.addTopLevelItem(item)

            # Directory:
            elif meta['type'] == 'Dir':
                self.stacked_pages.setCurrentWidget(self.icons_widget)
                self.icons_widget.setLayout(self.icons_layout)

                self.clear_layout(self.icons_layout)
                self.icons_layout.setAlignment(QtCore.Qt.AlignTop)

                # Request addition of 'file_name' to data model
                if 'full_path' in meta:
                    dir_path = meta['full_path']
                    files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
                    self.buttons.clear()
                    print(files)

                    for file in files:
                        file_name = file.split('.')[0]
                        button = QtWidgets.QPushButton(file_name)
                        self.buttons[file_name] = button

                        self.icons_layout.addWidget(button, self.row_index, self.column_index)
                        self.update_grid_positions()
                        self.set_button_style(button)

                        # signal-slot connection for file buttons:
                        button.clicked.connect(partial(self.on_item_clicked, dir_path + "\\" + file))

                    # file_name = os.path.basename(meta['full_path'])

    def on_item_clicked(self, file):   # request to add the parameter in stub

        print("Do something with: " + str(file))


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
        if self.column_index == 3:  # go to next row
            self.row_index += 1
            self.column_index = 0

    def set_button_style(self, button):
        button.setFixedSize(100, 30)
        # button.setStyleSheet("background-color : #FFF3F3")
        button.setStyleSheet("border - width: 0px")
        button.setStyleSheet("background : none")
        # button.setAlignment(QtCore.Qt.AlignCenter)
        button.setStyleSheet("QPushButton::hover"
                             "{"
                             "background-color : lightblue;"
                             "}")

    def setup_list_view(self):
        self.stacked_pages.setCurrentWidget(self.list_table)

    def setup_icons_view(self):
        self.stacked_pages.setCurrentWidget(self.icons_widget)













