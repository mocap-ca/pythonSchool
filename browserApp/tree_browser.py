""" This is a file browser that uses a FileItem object to show a tree of files """

from PyQt5 import QtWidgets, QtCore


class TreeBrowser(QtWidgets.QTreeWidget):

    def __init__(self, parent=None):
        super(TreeBrowser, self).__init__(parent)

    def populate(self, top_item):
        self.clear()
        for i in range(top_item.children()):
            child = top_item.get_child(i)
            item = QtWidgets.QTreeWidgetItem([child.short_name()])
            item.setData(0, QtCore.Qt.UserRole, child)
            self.addTopLevelItem(item)
