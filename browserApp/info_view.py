""" This will show detailed information about an item """

try:
    from PySide2 import QtWidgets, QtCore
    create_signal = QtCore.Signal
except:
    from PyQt5 import QtWidgets, QtCore
    create_signal = QtCore.pyqtSignal


class InfoView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(InfoView, self).__init__(parent)

        layout = QtWidgets.QHBoxLayout()

        self.table = QtWidgets.QTreeWidget()
        self.table.setColumnCount(2)

        layout.addSpacing(1)
        layout.addWidget(self.table)
        layout.addSpacing(1)


        self.setLayout(layout)

    def populate(self, data):
        print("Do something useful with: " + str(data))

        # Clear the table
        self.table.clear()

        # Update the table with name : value from the get_info() dict
        meta = data.get_info()
        for k, v in meta.items():
            item = QtWidgets.QTreeWidgetItem([k,v])
            self.table.addTopLevelItem(item)




