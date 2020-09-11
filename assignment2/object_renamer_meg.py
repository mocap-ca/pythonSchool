from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance

try:
  from PySide2 import QtWidgets, QtCore
except ImportError:
  from PyQt5 import QtWidgets, QtCore

import maya.cmds as m
import os

class MyDialog(QtWidgets.QDialog):
    def __init__(self):

        ptr = omui.MQtUtil.mainWindow()
        parent = wrapInstance(long(ptr), QtWidgets.QWidget)

        super(MyDialog, self).__init__(parent)

        main_layout = QtWidgets.QVBoxLayout()

        self.list = QtWidgets.QListWidget()
        main_layout.addWidget(self.list)

        self.button = QtWidgets.QPushButton("Button1")
        self.button.pressed.connect(self.b1)
        main_layout.addWidget(self.button)


        self.setLayout(main_layout)

        self.resize(400, 400)
        self.populate()


    def b1(self):
        print("BUTTON")

    def populate(self):
        self.list.clear()
        wd = m.workspace(q=True, rd=True)

        for i in os.listdir(os.path.join(wd, "scenes")):
            if i.startswith("."):
                continue

            if i.lower().endswith(".mb") or i.lower().endswith(".ma"):
                self.list.addItem(i)


INSTANCE = None
def show_gui():
    """ Singleton to create the gui if it doesn't exist, or show if it does """
    global INSTANCE
    if not INSTANCE:
        INSTANCE = MyDialog()
    INSTANCE.show()
    return INSTANCE