import sys
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore

class InviteDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):        # Constructor
        super(InviteDialog, self).__init__(parent)

        self.overallLayout = QtWidgets.QVBoxLayout()
        self.overallWidget = QtWidgets.QStackedWidget()
        self.inviteWidget = QtWidgets.QWidget()
        self.closingWidget = QtWidgets.QWidget()
        self.overallLayout.addWidget(self.overallWidget)

        #          ----------------- Invite Widget ------------------------
        self.inviteLayout = QtWidgets.QVBoxLayout()

        self.imgLabel = QtWidgets.QLabel(self)
        self.imgLabel.setPixmap("party.jpg")
        self.imgLabel.setMaximumWidth(400)
        self.welcomeText = QtWidgets.QLabel("Just a party.\nDrinks and pizza.\nSaturday 7pm.\n\n\n")
        self.welcomeText.setAlignment(QtCore.Qt.AlignCenter)

        self.rsvpYesButton = QtWidgets.QPushButton("Yeaahh! Let's do this.")
        self.rsvpYesButton.pressed.connect(self.yesBtnFtn)
        self.rsvpMaybeButton = QtWidgets.QPushButton("Cool. Let's see. Maybe.")
        self.rsvpMaybeButton.pressed.connect(self.maybeBtnFtn)
        self.rsvpNoButton = QtWidgets.QPushButton("Nah man, I got other things.")
        self.rsvpNoButton.pressed.connect(self.noBtnFtn)
        self.setLayout(self.inviteLayout)
        self.setWindowTitle("Ginger and Olive's Party Invite")

        self.inviteLayout.addWidget(self.imgLabel)
        self.inviteLayout.addWidget(self.welcomeText)
        self.inviteLayout.addWidget(self.rsvpYesButton)
        self.inviteLayout.addWidget(self.rsvpNoButton)
        self.inviteLayout.addWidget(self.rsvpMaybeButton)

        self.inviteWidget.setLayout(self.inviteLayout)

        #          ----------------- Closing Widget ------------------------
        self.closingLabel = QtWidgets.QLabel()
        self.backLabel = QtWidgets.QLabel("Back")
        self.closingLayout = QtWidgets.QVBoxLayout()
        self.closingLayout.addWidget(self.closingLabel)
        self.closingLayout.addWidget(self.backLabel)
        self.closingWidget.setLayout(self.closingLayout)
        #          --------------------------------------------------------

        self.overallWidget.addWidget(self.inviteWidget)
        self.overallWidget.addWidget(self.closingWidget)
        self.overallWidget.setCurrentWidget(self.inviteWidget)

        self.setLayout(self.overallLayout)

    def yesBtnFtn(self):
        self.closingLabel.setText('See you then.')
        self.closingTemplate()

    def noBtnFtn(self):
        print("Okay.")
        self.closingLabel.setText('Okay.')
        self.closingLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.overallWidget.setCurrentWidget(self.closingWidget)

    def maybeBtnFtn(self):
        print("Ok. Lemme know.")
        self.closingLabel.setText('Ok, lemme know.')
        self.closingLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.overallWidget.setCurrentWidget(self.closingWidget)

    def closingTemplate(self):
        self.closingLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.overallWidget.setCurrentWidget(self.closingWidget)
        self.rsvpNoButton.pressed.connect(self.noBtnFtn)
        QtCore.QObject.connect(self.backLabel, QtCore.SIGNAL(_fromUtf8("clicked()")), self.goBack())

    def goBack(self):
        print("go back")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    inviteDialog = InviteDialog()   # creating an instance of class InviteDialog, running constructor
    inviteDialog.exec_()





