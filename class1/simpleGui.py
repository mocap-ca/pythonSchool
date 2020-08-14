import sys
try:
  from PySide2 import QtWidgets, QtCore
except ImportError:
  from PyQt5 import QtWidgets, QtCore

import maya.cmds as m
import os

class MyDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)

        self.status = None

        # browse bar
        browse_layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Path:")

        button = QtWidgets.QPushButton("browse")
        button.pressed.connect(self.do_something)

        self.path_field = QtWidgets.QLineEdit()

        browse_layout.addWidget(label)
        browse_layout.addWidget(self.path_field)
        browse_layout.addWidget(button)

        # main layout

        main_layout = QtWidgets.QVBoxLayout()

        self.list_widget = QtWidgets.QListWidget()

        self.list_widget.itemClicked.connect(self.table_click_event)

        main_layout.addItem(browse_layout)
        main_layout.addWidget(self.list_widget)

        self.setLayout(main_layout)
        self.resize(400, 400)

        self.populate()

    def populate(self):
        for shapeNode in m.ls(type="mesh", l=True):

            name = shapeNode
            if '|' in name:
                name = name[name.rfind('|')+1:]
            item = QtWidgets.QListWidgetItem(name)
            item.setData(QtCore.Qt.UserRole, shapeNode)
            self.list_widget.addItem(item)


    def do_something(self):

        ret = QtWidgets.QFileDialog.getExistingDirectory(self, "find me a directory")
        print("Returned: " + str(ret) + " type: " + str(type(ret)))
        if ret:
            self.path_field.setText(ret)
            self.status = True

            for i in os.listdir(ret):
                if not i.lower().endswith(".py"):
                    continue

                item = QtWidgets.QListWidgetItem(i)
                item.setData(QtCore.Qt.UserRole, os.path.join(ret, i))
                item.setData(QtCore.Qt.UserRole + 1, "BLOOP")
                self.list_widget.addItem(item)

    def table_click_event(self, item):

        print("CLICK!")
        print(item.data(QtCore.Qt.UserRole))
        print(item.data(QtCore.Qt.UserRole +1))




def blah():
    print("hello")



if __name__ == "__main__":

    blah()

    #aapp = QtWidgets.QApplication(sys.argv)
    #d = MyDialog()
    #d.exec_()
