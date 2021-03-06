""" This is a file browser that uses a FileItem object to show a tree of files """

try:
    from PySide2 import QtWidgets, QtCore, QtGui
    create_signal = QtCore.Signal
except:
    from PyQt5 import QtWidgets, QtCore, QtGui
    create_signal = QtCore.pyqtSignal

from browserApp.model import base


class TreeBrowser(QtWidgets.QTreeWidget):

    app_item_selected = create_signal(base.BaseItem)

    def __init__(self, parent=None):
        super(TreeBrowser, self).__init__(parent)
        self.itemExpanded.connect(self.on_item_expanded)
        self.itemClicked.connect(self.on_item_clicked)

    def populate(self, top_item):
        self.clear()
        self.top_item = top_item
        self.setHeaderHidden(True)

        if 'full_path' in self.top_item.get_info():
            self.setHeaderLabel(top_item.get_info()['full_path'])
        else:
            self.setHeaderHidden(True)

        for i in range(top_item.children()):
            child = top_item.get_child(i)
            item = QtWidgets.QTreeWidgetItem([child.short_name()])
            item.setData(0, QtCore.Qt.UserRole, child)
            self.addTopLevelItem(item)
            self.add_icon(item)
            self.add_children(item)

    def on_item_expanded(self, item):
        for i in range(item.childCount()):
            child = item.child(i)
            self.add_children(child)

    def on_item_clicked(self, item):
        model_item = item.data(0, QtCore.Qt.UserRole)
        self.app_item_selected.emit(model_item)

    def add_children(self, widget_item):
        item = widget_item.data(0, QtCore.Qt.UserRole)
        for i in range(item.children()):
            child = item.get_child(i)
            child_widget_item = QtWidgets.QTreeWidgetItem([child.short_name()])
            child_widget_item.setData(0, QtCore.Qt.UserRole, child)
            widget_item.addChild(child_widget_item)
            self.add_icon(child_widget_item)

    def add_icon(self, item):
        data = item.data(0, QtCore.Qt.UserRole)
        data_type = data.get_info()['type']
        if data_type == 'File':
            icon = self.style().standardPixmap(QtWidgets.QStyle.SP_FileIcon)
        elif data_type == 'Dir':
            icon = self.style().standardPixmap(QtWidgets.QStyle.SP_DirIcon)
        else:
            icon = None
        item.setIcon(0, QtGui.QIcon(icon))

