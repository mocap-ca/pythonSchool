# coding=utf-8

""" This will show detailed information about an item """

import sys
import os
import pprint
import time

try:
    from PySide2 import QtWidgets, QtCore, QtGui
except:
    from PyQt5 import QtWidgets, QtCore, QtGui


class BrowserDialog(QtWidgets.QDialog):
    def __init__(self, folder_path, parent=None):
        """

        """
        super(BrowserDialog, self).__init__(parent)

        self.setWindowTitle("File Browser 1.0 © CollabMLM 2020")
        self.setGeometry(600, 300, 700, 400)

        self.folder_path = folder_path

        # Data
        self.list_of_file_details = []

        # Dialog layout
        self.dialog_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.dialog_layout)

        self.left_widget = QtWidgets.QWidget()
        self.right_widget = QtWidgets.QWidget()

        self.dialog_layout.addWidget(self.left_widget)
        self.dialog_layout.addWidget(self.right_widget)

        self.left_layout = QtWidgets.QVBoxLayout()
        self.right_layout = QtWidgets.QVBoxLayout()

        self.left_widget.setLayout(self.left_layout)
        self.right_widget.setLayout(self.right_layout)

        # Left Widget
        self.icon_list_buttons_bar_widget = QtWidgets.QWidget()
        self.icon_list_buttons_bar_layout = QtWidgets.QHBoxLayout()
        self.scroll_area_widget = QtWidgets.QScrollArea()
        self.page_stack_widget = QtWidgets.QStackedWidget()
        self.icons_button = QtWidgets.QPushButton("Icon View")
        self.icons_button.pressed.connect(self.display_icon_view)
        self.list_button = QtWidgets.QPushButton("List View")
        self.list_button.pressed.connect(self.display_list_view)
        # Icons page
        self.icon_page_widget = QtWidgets.QWidget()
        self.icon_page_layout = QtWidgets.QVBoxLayout()
        # List page
        self.list_page_widget = QtWidgets.QWidget()
        self.list_grid_layout = QtWidgets.QGridLayout()

        # Right Widget
        self.file_details_widget = QtWidgets.QListWidget()
        self.default_details_label = QtWidgets.QLabel()

        self.setup_left_widget()
        self.setup_right_widget()

        self.setup_style()

        self.populate()

    def setup_style(self):
        self.right_widget.setMaximumWidth(200)
        self.icons_button.setMaximumWidth(70)
        self.list_button.setMaximumWidth(70)
        self.icon_list_buttons_bar_layout.setAlignment(QtCore.Qt.AlignLeft)

    def populate(self):
        self.list_of_file_detail_dictionaries = []
        for file in os.listdir(self.folder_path):
            full_path = os.path.join(self.folder_path, file)
            each_file = {
                "full_path": full_path,
                "name": file,
                "type": str(file).split(".")[-1],
                "size": os.stat(full_path).st_size,
                "date_and_time_created": time.ctime(os.path.getctime(full_path))}
            self.list_of_file_detail_dictionaries.append(each_file)
        pprint.pprint(self.list_of_file_detail_dictionaries)


    def setup_left_widget(self):
        # Icon and List Buttons Bar:
        self.left_layout.addWidget(self.icon_list_buttons_bar_widget)
        self.icon_list_buttons_bar_widget.setLayout(self.icon_list_buttons_bar_layout)
        self.icon_list_buttons_bar_layout.addWidget(self.icons_button)
        self.icon_list_buttons_bar_layout.addWidget(self.list_button)

        # Scrollable area:
        self.left_layout.addWidget(self.page_stack_widget)
        self.page_stack_widget.addWidget(self.icon_page_widget)
        self.page_stack_widget.addWidget(self.list_page_widget)
        self.page_stack_widget.setCurrentWidget(self.icon_page_widget)

    def setup_right_widget(self):
        self.right_layout.addWidget(self.default_details_label)
        self.right_layout.addWidget(self.file_details_widget)
        self.default_details_label.setText("Select a file to see details.")

    def display_icon_view(self):
        pass
        # self.icon_page_widget.setLayout(self.icon_page_layout)
        # for item in self.list_of_file_detail_dictionaries:


    def display_list_view(self):
        pass
        # self.list_page_widget.setLayout(self.list_page_layout)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    folder_path = "/Volumes/T7/GhostKid"
    browser_dialog = BrowserDialog(folder_path)
    browser_dialog.exec_()
