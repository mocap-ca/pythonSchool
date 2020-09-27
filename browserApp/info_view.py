""" This will show detailed information about an item """

from PyQt5 import QtWidgets


class InfoView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(InfoView, self).__init__(parent)

        layout = QtWidgets.QHBoxLayout()

        layout.addSpacing(1)
        layout.addWidget(QtWidgets.QLabel("info goes here"))
        layout.addSpacing(1)

        self.setLayout(layout)

    def populate(self, data):
        print("Do something useful with: " + str(data))



