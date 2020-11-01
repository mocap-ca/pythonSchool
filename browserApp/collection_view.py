""" This will show detailed information about an item """

try:
    from PySide2 import QtWidgets, QtCore
except:
    from PyQt5 import QtWidgets, QtCore


class CollectionView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CollectionView, self).__init__(parent)

        self.layout = QtWidgets.QHBoxLayout()
        self.hide()
        self.setLayout(self.layout)

    def populate(self, items):
        self.clear()
        child_count = items.children()
        if child_count == 0:
            self.hide()
            return

        self.show()

        keys = set()
        integer_values = {}

        # Get keys
        for i in range(child_count):
            subitem = items.get_child(i)
            meta = subitem.get_info()
            keys.update(meta.keys())

        # Get cumulative key values
        for i in range(child_count):
            subitem = items.get_child(i)
            meta = subitem.get_info()

            for key in [x for x in keys if x in meta]:
                value = meta[key]
                if isinstance(value, int):
                    if key not in integer_values:
                        integer_values[key] = 0
                    integer_values[key] += value

        for key, value in integer_values.items():
            print(str(key) + str(value))
            label = QtWidgets.QLabel("Total {}: {}".format(key, value))
            self.layout.addWidget(label)

    def clear(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.clear()





