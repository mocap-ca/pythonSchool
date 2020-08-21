import sys
try:
  from PySide2 import QtWidgets, QtCore
except ImportError:
  from PyQt5 import QtWidgets, QtCore

from functools import partial

class MyDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)
        layout = QtWidgets.QHBoxLayout()
        self.cb1 = QtWidgets.QCheckBox("One")
        self.cb1.stateChanged.connect(partial(self.checkbox_event, "ONE"))
        self.cb2 = QtWidgets.QCheckBox("Two")
        self.cb2.stateChanged.connect(self.checkbox_event)
        self.cb3 = QtWidgets.QCheckBox("Three")
        self.cb3.stateChanged.connect(self.checkbox_event)
        layout.addWidget(self.cb1)
        layout.addWidget(self.cb2)
        layout.addWidget(self.cb3)
        self.setLayout(layout)
        self.resize(400, 400)

    def checkbox_event(self, ref, value):

        if value & QtCore.Qt.Checked:
            print("Checked!  " + str(ref))
        else:
            print("Unchecked")

def show_dialog():
    app = QtWidgets.QApplication(sys.argv)
    d = MyDialog()
    d.exec_()


if __name__ == "__main__":
    show_dialog()
