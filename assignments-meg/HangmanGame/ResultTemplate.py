import sys
from PySide2 import QtWidgets, QtCore, QtGui


class ResultClass(QtWidgets.QDialog):
    def __init__(self, parent=None):
        """Sets up the widgets in the Result template.
        :param: parent :  provides ability to connect to external applications like Maya.
        :param type: QWidget."""
        super(ResultClass, self).__init__(parent)
        self.result = ""
        self.result_layout = QtWidgets.QVBoxLayout()
        self.result_label = QtWidgets.QLabel()
        self.result_font = QtGui.QFont()

    def setup_result_layout(self):
        """Sets up layout to display a final message on the result page."""
        self.result_label.setFont(self.result_font)
        if self.result == "error":
            self.result_label.setText("All questions are away in meetings. Come back later.")
        if self.result == "success":
            self.result_label.setText("Well played! But damn, stop watching so many movies. Do some work.")
        elif self.result == "failure":
            self.result_label.setText("All those wrong guesses! SMH. Start over.")
        self.result_label.setAlignment(QtCore.Qt.AlignCenter)
        self.result_layout.addWidget(self.result_label)
