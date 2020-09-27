""" This is the main application that implments everything in an abstract way """

from PyQt5 import QtWidgets, QtCore
import sys

from browserApp import info_view, tree_browser, collection_view
from browserApp.model import file as model_file


class App(QtWidgets.QMainWindow):

    """ This is the base application, which should work with any kind of model data """

    def __init__(self, top_item, parent=None):
        super(App, self).__init__(parent)

        self.top_item = top_item

        # Create a main widget
        self.main_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.main_widget)

        layout = QtWidgets.QHBoxLayout()

        # Tree View (on left)
        self.tree = tree_browser.TreeBrowser()
        self.tree.app_item_selected.connect(self.itemSelected)
        layout.addWidget(self.tree)

        # Collection view (in middle)
        self.collection = collection_view.CollectionView()
        layout.addWidget(self.collection)

        # Info view (on right)
        self.info = info_view.InfoView()
        layout.addWidget(self.info)

        self.main_widget.setLayout(layout)

        self.tree.populate(self.top_item)

        self.resize(800, 500)

        self.show()


    def itemSelected(self, model_info):
        """ User as clicked on an item in the tree, pass item's data to the info view """
        self.info.populate(model_info)
        self.collection.populate(model_info)




def show_app(top_item):
    app = QtWidgets.QApplication(sys.argv)
    win = App(top_item)
    app.exec_()  # blocking call


if __name__ == "__main__":
    top_item = model_file.FileItem("/Volumes/T7/GhostKid")

    show_app(top_item)