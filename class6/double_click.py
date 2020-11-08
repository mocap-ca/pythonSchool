import sys
try:
  from PySide2 import QtWidgets, QtCore
except ImportError:
  from PyQt5 import QtWidgets, QtCore

from functools import partial

class MyButton(QtWidgets.QLabel):

    selected = QtCore.pyqtSignal()
    do_action = QtCore.pyqtSignal(str)

    def __init__(self, text, meta, parent):
        super(MyButton, self).__init__(parent)
        self.setText(text)
        self.meta = meta

    def mouseDoubleClickEvent(self, event):
        self.do_action.emit(self.meta)

    def mousePressEvent(self, event):
        self.setSelected(True)
        self.selected.emit()

    def setSelected(self, value):
        if value:
            self.setStyleSheet("background: blue")
        else:
            self.setStyleSheet("")

        print("single")




class MyDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)
        layout = QtWidgets.QHBoxLayout()
        self.cb1 = QtWidgets.QCheckBox("One")
        self.cb1.stateChanged.connect(partial(self.checkbox_event, "ONE"))
        self.cb2 = QtWidgets.QCheckBox("Two")
        self.cb2.stateChanged.connect(partial(self.checkbox_event, "TWO"))
        self.cb3 = QtWidgets.QCheckBox("Three")
        self.cb3.stateChanged.connect(partial(self.checkbox_event, "THREE"))

        self.b1 = MyButton('test1', 'file1', self)
        self.b2 = MyButton('test2', 'file2', self)

        self.b1.selected.connect(partial(self.b2.setSelected, False))
        self.b2.selected.connect(partial(self.b1.setSelected, False))


        layout.addWidget(self.cb1)
        layout.addWidget(self.cb2)
        layout.addWidget(self.cb3)
        layout.addWidget(self.b1)
        layout.addWidget(self.b2)
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
