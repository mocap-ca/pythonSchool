""" This is the main application that implments everything in an abstract way """

from PyQt5 import QtWidgets, QtCore
import sys

from browserApp import info_view, tree_browser


class App(QtWidgets.QMainWindow):

    """ This is the base application, which should work with any kind of model data """

    def __init__(self, top_item, parent=None):
        super(App, self).__init__(parent)

        self.top_item = top_item

        # Create a main widget
        self.main_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.main_widget)

        layout = QtWidgets.QHBoxLayout()

        self.tree = tree_browser.TreeBrowser()
        self.tree.itemClicked.connect(self.itemSelected)

        layout.addWidget(self.tree)

        self.info = info_view.InfoView()
        layout.addWidget(self.info)

        self.main_widget.setLayout(layout)

        self.tree.populate(self.top_item)

        self.resize(800, 500)

        self.show()


    def itemSelected(self, item, col):
        """ User as clicked on an item in the tree, pass item's data to the info view """
        model_info = item.data(0, QtCore.Qt.UserRole).get_info()
        self.info.populate(model_info)




def show_app(top_item):
    app = QtWidgets.QApplication(sys.argv)
    win = App(top_item)
    app.exec_()  # blocking call


if __name__ == "__main__":
    show_app()