import sys
from PySide2 import QtWidgets


class MyDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)
        layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel("Hello")
        layout.addWidget(label)
        self.setLayout(layout)
        self.resize(400, 400)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    d = MyDialog()
    d.exec_()
