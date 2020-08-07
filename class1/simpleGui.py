import sys
from PySide2 import QtWidgets


class MyDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)
        layout = QtWidgets.QHBoxLayout()
        self.label1 = QtWidgets.QLabel("Hello Label 1")
        self.label2 = QtWidgets.QLabel("Hello Label 2")
        self.label3 = QtWidgets.QLabel("Hello Label 3")
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        layout.addWidget(self.label3)
        self.setLayout(layout)
        self.resize(400, 400)


def show_dialog():
    app = QtWidgets.QApplication(sys.argv)
    d = MyDialog()
    d.label1.setText("HELLO!!!")
    print(d.label1.text())
    d.exec_()  # blocking call


if __name__ == "__main__":
    show_dialog()
