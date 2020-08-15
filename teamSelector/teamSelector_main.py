


import sys
from PySide2 import QtWidgets

class ssDialog(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(ssDialog, self).__init__(parent)

        # Layouts
        main_layout = QtWidgets.QHBoxLayout()
        home_layout = QtWidgets.QVBoxLayout()
        away_layout = QtWidgets.QVBoxLayout()


        # Widgets
        home_label = QtWidgets.QLabel("Home team:")
        away_label = QtWidgets.QLabel("Away team:")
        self.home_country_cb = QtWidgets.QComboBox()





        self.button1 = QtWidgets.QPushButton("Go")
        self.label_name1 = QtWidgets.QLabel("Team Name:")

        # setup
        mainLayout.addWidget(self.label_name1)
        mainLayout.addWidget(self.button1)

        self.setLayout(mainLayout)

    def lower_case(self, name = "Test Name"):
        return name.replace(" ", "_").lower()

def show_dialog():
    app = QtWidgets.QApplication(sys.argv)
    d = ssDialog()
    d.exec_()  # blocking call


if __name__ == "__main__":
    show_dialog()
