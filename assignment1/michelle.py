#import maya.cmds as mc
from PySide2 import QtCore
from PySide2 import QtWidgets



class ImportWin(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ImportWin, self).__init__(parent)
        '''Window details. Setting window name and minimum size'''
        self.setWindowTitle("Import")
        self.resize(400,400)

        '''Create widgets'''
        self.dir_path = QtWidgets.QLineEdit()
        self.browse_button = QtWidgets.QPushButton("Browse Path")
        #self.import_button = QtWidgets.QPushButton("Import files")


        '''Create label for widgets'''

        '''Set layout for widgets'''
        self.layout = QtWidgets.QHBoxLayout()

        '''Create event for widgets when clicked'''
        self.browse_button.clicked.connect(self.open_dir)

        '''Adding widgets and setting the layout'''
        self.layout.addWidget(self.dir_path)
        self.layout.addWidget(self.browse_button)
        #self.layout.addWidget(self.import_button)
        self.setLayout(self.layout)

    def open_dir(self):
        '''When browse button is pushed, select directory path to browse. Dir path will be set
        in QLineEdit field'''
        dir = QtWidgets.QFileDialog.getExistingDirectory(self,"Find Directory..." )
        correct_path = self.dir_path.setText(dir)
        return correct_path #how to return the dir path name??





if __name__ == "__main__": # this is when your program start
    d = ImportWin()
    d.show()
