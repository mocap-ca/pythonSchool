import sys
from PySide2 import QtWidgets, QtCore, QtGui


class WelcomeClass(QtWidgets.QDialog):
    def __init__(self, parent=None):
        """Sets up the widgets in the Welcome template.
        :param: parent :  provides ability to connect to external applications like Maya.
        :param type: QWidget."""
        super(WelcomeClass, self).__init__(parent)
        self.welcome_layout = QtWidgets.QVBoxLayout()
        self.welcome_label = QtWidgets.QLabel("Welcome to Hangman! Are you ready?")
        self.enter_button = QtWidgets.QPushButton("Enter")
        self.welcome_font = QtGui.QFont()

    def setup_welcome_layout(self):
        """Sets up layout to display a welcome message, and an "Enter" button."""
        self.enter_button.setMaximumWidth(300)
        self.welcome_label.setFont(self.welcome_font)
        self.enter_button.setFont(self.welcome_font)
        self.welcome_layout.addWidget(self.welcome_label)
        self.welcome_layout.addWidget(self.enter_button)
        self.welcome_layout.setAlignment(QtCore.Qt.AlignCenter)
