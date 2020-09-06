#import maya.cmds as mc
from PySide2 import QtCore
from PySide2 import QtWidgets



class RigWin(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(RigWin, self).__init__(parent)

        '''Window details. Setting window name and minimum size'''
        self.setWindowTitle("Rigging Tools")
        self.setMinimumSize(400)

        self.create_widget()
        self.create_layout()

        '''Creating all widgets under a function'''
        def create_widget(self):
            self.button_one = QtWidgets.QPushButton("Push Me")

        '''Parents widgets from create_widget function to layout. 
        Widgets need to be parented to the layout in order for them to
        be visible and added to the window'''
        def create_layout(self):
            layout = QtWidgets.QVBoxLayout()
            layout.addWidget(self.button_one)

        #
        #
        # layout.addWidget(self.button_one)
        #
        # self.layout()




if __name__ == "__main__": # this is when your program start
    d = RigWin()
    d.show()
