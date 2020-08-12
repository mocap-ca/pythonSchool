import sys
from PySide2 import QtWidgets


class MyDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)

        # layouts
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.leftLayout = QtWidgets.QVBoxLayout()
        self.rightLayout = QtWidgets.QVBoxLayout()
        self.candidateLayout = QtWidgets.QVBoxLayout()
        self.name1Layout = QtWidgets.QHBoxLayout()
        self.name2Layout = QtWidgets.QHBoxLayout()
        self.acceptRejectFrame = QtWidgets.QFrame()
        self.acceptRejectFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.acceptRejectFrame.setStyleSheet("background-color: rgb(210,210,210);")
        self.acceptRejectLayout = QtWidgets.QHBoxLayout(self.acceptRejectFrame)
        self.jobLayout = QtWidgets.QHBoxLayout()
        self.jobLevelLayout = QtWidgets.QVBoxLayout()
        self.jobTypeLayout = QtWidgets.QHBoxLayout()
        self.responseLayout = QtWidgets.QVBoxLayout()

        # widgets
        self.button_one = QtWidgets.QPushButton("Generate Response")
        self.button_one.pressed.connect(self.button_pressed)
        self.label_candidate = QtWidgets.QLabel("Candidate:")
        self.label_name1 = QtWidgets.QLabel("First Name:")
        self.le_name1 = QtWidgets.QLineEdit()
        self.label_name2 = QtWidgets.QLabel("Last Name:")
        self.le_name2 = QtWidgets.QLineEdit()
        self.cb_title = QtWidgets.QComboBox(self)
        title_list = ["Mr",
                     "Mrs",
                     "Ms",
                     "Mx",
                     "Dr",
                     "Prof"]
        self.cb_title.addItems(title_list)
        self.displayText = QtWidgets.QLabel("")
        self.rb_accept = QtWidgets.QRadioButton("Accept")
        self.rb_reject = QtWidgets.QRadioButton("Reject")
        self.rb_recall = QtWidgets.QRadioButton("Recall")
        self.rbGroup_acceptReject = QtWidgets.QButtonGroup()
        self.rbGroup_acceptReject.addButton(self.rb_accept)
        self.rbGroup_acceptReject.addButton(self.rb_reject)
        self.rbGroup_acceptReject.addButton(self.rb_recall)
        self.rb_junior = QtWidgets.QRadioButton("Junior")
        self.rb_mid = QtWidgets.QRadioButton("Mid")
        self.rb_senior = QtWidgets.QRadioButton("Senior")
        self.rbGroup_jobLevel = QtWidgets.QButtonGroup()
        self.rbGroup_jobLevel.addButton(self.rb_junior)
        self.rbGroup_jobLevel.addButton(self.rb_mid)
        self.rbGroup_jobLevel.addButton(self.rb_senior)
        self.list_jobType = QtWidgets.QListWidget()
        jobs_list = ["Roto",
                    "Layout",
                    "Matchmove",
                    "Modelling",
                    "Rigging",
                    "Animator",
                    "DMP",
                    "FX",
                    "CFX",
                    "Lighting",
                    "Pipeline"]
        self.list_jobType.addItems(jobs_list)
        self.te_response = QtWidgets.QTextEdit()
        self.label_response = QtWidgets.QLabel("Response Text:")

        # mainLayout
        self.mainLayout.addLayout(self.leftLayout)
        self.mainLayout.addLayout(self.rightLayout)
        self.mainLayout.addStretch()
        self.setLayout(self.mainLayout)
        self.resize(600, 150)

        # leftLayout
        self.leftLayout.addLayout(self.candidateLayout)
        self.candidateLayout.addWidget(self.label_candidate)
        self.candidateLayout.addWidget(self.cb_title)
        self.candidateLayout.addLayout(self.name1Layout)
        self.candidateLayout.addLayout(self.name2Layout)
        self.name1Layout.addWidget(self.label_name1)
        self.name1Layout.addWidget(self.le_name1)
        self.name2Layout.addWidget(self.label_name2)
        self.name2Layout.addWidget(self.le_name2)
        self.candidateLayout.addWidget(self.acceptRejectFrame)
        self.candidateLayout.addLayout(self.acceptRejectLayout)
        self.acceptRejectLayout.addWidget(self.rb_accept)
        self.acceptRejectLayout.addWidget(self.rb_reject)
        self.acceptRejectLayout.addWidget(self.rb_recall)
        self.candidateLayout.addSpacing(10)
        self.candidateLayout.addLayout(self.jobLayout)
        self.jobLayout.addLayout(self.jobLevelLayout)
        self.jobLayout.addLayout(self.jobTypeLayout)
        self.jobLevelLayout.addWidget(self.rb_junior)
        self.jobLevelLayout.addWidget(self.rb_mid)
        self.jobLevelLayout.addWidget(self.rb_senior)
        self.jobTypeLayout.addWidget(self.list_jobType)
        self.candidateLayout.addWidget(self.button_one)

        # rightLayout
        self.rightLayout.addLayout(self.responseLayout)
        self.responseLayout.addWidget(self.label_response)
        self.responseLayout.addWidget(self.te_response)

    def button_pressed(self):
        self.te_response.setText(self.get_display_string())

    def get_display_string(self):
        display_string = "Button pressed"
        greeting = "Dear " + self.cb_title.currentText() + " " + self.le_name1.text() + " " + self.le_name2.text() + ","

        if self.rb_junior.isChecked():
            jobTitle = "Junior"
        elif self.rb_mid.isChecked():
            jobTitle = "Mid"
        else:
            jobTitle = "Senior"

        jobTitle += " " + self.list_jobType.currentItem().text()

        if self.rb_reject.isChecked():
            result = "I regret to inform you that your application has not been successful."
        elif self.rb_accept.isChecked():
            result = "I am delighted to accept your application."
        else:
            result = "We would like to call you in for an interview."

        sign_off = "Kind regards, \nDisney"

        display_string = greeting + "\n\n" + "Regarding job: " + jobTitle + "\n\n" + result + "\n\n" + sign_off

        return display_string

    def text_has_changed(self, value):
        self.displayText.setText("Output: " + value)


def show_dialog():
    app = QtWidgets.QApplication(sys.argv)
    d = MyDialog()
    d.setStyleSheet("background-color: rgb(180, 180, 180)")
    d.exec_()  # blocking call


if __name__ == "__main__":
    show_dialog()
