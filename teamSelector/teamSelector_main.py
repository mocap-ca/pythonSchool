import sys
from PySide2 import QtWidgets

class ssDialog(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(ssDialog, self).__init__(parent)

        # Layouts
        mainLayout = QtWidgets.QHBoxLayout()

        # Widgets
        self.button1 = QtWidgets.QPushButton("Go")
        self.label_name1 = QtWidgets.QLabel("Team Name:")

        # setup
        mainLayout.addWidget(self.label_name1)
        mainLayout.addWidget(self.button1)

        self.setLayout(mainLayout)


def show_dialog():
    app = QtWidgets.QApplication(sys.argv)
    d = ssDialog()
    d.exec_()  # blocking call


if __name__ == "__main__":
    show_dialog()
