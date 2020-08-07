import sys
from PySide2 import QtWidgets


class MyDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)
        layout = QtWidgets.QVBoxLayout()
        self.label1 = QtWidgets.QLabel("Hello Label 1")
        self.button_one = QtWidgets.QPushButton("Press Me!")
        self.button_one.pressed.connect(self.button_pressed)
        self.line_edit = QtWidgets.QLineEdit("Text Goes Here", self)
        self.line_edit.textChanged.connect(self.text_has_changed)
        layout.addWidget(self.label1)
        layout.addWidget(self.button_one)
        layout.addWidget(self.line_edit)
        layout.addStretch()
        self.setLayout(layout)
        self.resize(300, 150)

    def button_pressed(self):
        print("HERE!")

    def text_has_changed(self, value):
        self.label1.setText("Text is: " + value)


def show_dialog():
    app = QtWidgets.QApplication(sys.argv)
    d = MyDialog()
    print(d.button_one)
    d.exec_()  # blocking call


if __name__ == "__main__":
    show_dialog()
