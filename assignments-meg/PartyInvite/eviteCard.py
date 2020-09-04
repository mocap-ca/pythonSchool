import sys
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore

class InviteDialog(QtWidgets.QDialog):
    """This class creates all the necessary UI for the invite dialog.
    Displays a welcome message. Provides three rsvp options to the user : yes, no and maybe.
    Based on the chosen rsvp, displays a closing message."""

    def __init__(self, parent=None):
        """Sets up the main UI framework.
        Creates a stacked widget for the welcome and closing pages.
        :param parent: Gives the ability to connect to external application such as Maya
        :type parent: QWidget"""
        super(InviteDialog, self).__init__(parent)

        self.overall_layout = QtWidgets.QVBoxLayout()
        self.overall_widget = QtWidgets.QStackedWidget()
        self.overall_layout.addWidget(self.overall_widget)

        self.setup_invite_widget()
        self.setup_closing_widget()
        self.add_widgets_to_stack()

        self.setLayout(self.overall_layout)
        self.setWindowTitle("Ginger and Jam's Party Invite")

    def setup_invite_widget(self):
        """Sets up the invite page, which contains an image label, some text on a label, and the rsvp buttons. """
        self.invite_widget = QtWidgets.QWidget()
        self.invite_layout = QtWidgets.QVBoxLayout()

        self.setup_image_label()
        self.setup_text_label()
        self.setup_rsvp_buttons()

        self.add_widgets_to_invite()
        self.invite_widget.setLayout(self.invite_layout)

    def setup_closing_widget(self):
        """Sets up the closing page, which contains a closing label"""
        self.closing_widget = QtWidgets.QWidget()
        self.closing_label = QtWidgets.QLabel()
        self.closing_layout = QtWidgets.QVBoxLayout()

    def add_widgets_to_stack(self):
        """Adds the invite and closing pages to the stack. Sets the current widget to invite page."""
        self.overall_widget.addWidget(self.invite_widget)
        self.overall_widget.addWidget(self.closing_widget)
        self.overall_widget.setCurrentWidget(self.invite_widget)

    def setup_rsvp_buttons(self):
        """Creates three rsvp buttons and sets up the signal-slot connections"""
        self.rsvp_yes_button = QtWidgets.QPushButton("Yeaahh! Let's do this.")
        self.rsvp_yes_button.pressed.connect(self.yes_button_logic)
        self.rsvp_maybe_button = QtWidgets.QPushButton("Cool. Let's see. Maybe.")
        self.rsvp_maybe_button.pressed.connect(self.maybe_button_logic)
        self.rsvp_no_button = QtWidgets.QPushButton("Nah man, I got other things.")
        self.rsvp_no_button.pressed.connect(self.no_button_logic)

    def setup_image_label(self):
        """Loads the label with the image and sets its dimensions"""
        self.img_label = QtWidgets.QLabel(self)
        self.img_label.setPixmap("party.jpg")
        self.img_label.setMaximumWidth(400)

    def setup_text_label(self):
        """Creates a welcome label and adds a message to it"""
        self.welcome_text = QtWidgets.QLabel("Just a party.\nDrinks and pizza.\nSaturday 7pm.\n\n\n")
        self.welcome_text.setAlignment(QtCore.Qt.AlignCenter)

    def add_widgets_to_invite(self):
        self.invite_layout.addWidget(self.img_label)
        self.invite_layout.addWidget(self.welcome_text)
        self.invite_layout.addWidget(self.rsvp_yes_button)
        self.invite_layout.addWidget(self.rsvp_no_button)
        self.invite_layout.addWidget(self.rsvp_maybe_button)


    def yes_button_logic(self):
        """Adds a closing message for when the user rsvps 'yes'"""
        self.closing_label.setText('See you then.')
        self.closing_widget_logic()

    def no_button_logic(self):
        """Adds a closing message for when the user rsvps 'no'"""
        self.closing_label.setText('Okay.')
        self.closing_widget_logic()

    def maybe_button_logic(self):
        """Adds a closing message for when the user rsvps 'maybe'"""
        self.closing_label.setText('Ok, lemme know.')
        self.closing_widget_logic()

    def closing_widget_logic(self):
        """Sets the current stack widget to closing page, and adds the closing label to it"""
        self.closing_layout.addWidget(self.closing_label)
        self.closing_widget.setLayout(self.closing_layout)
        self.closing_label.setAlignment(QtCore.Qt.AlignCenter)
        self.overall_widget.setCurrentWidget(self.closing_widget)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    invite_dialog = InviteDialog()   # creating an instance of class InviteDialog, running constructor
    invite_dialog.exec_()





