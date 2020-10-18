""" This will show detailed information about an item """

try:
    from PySide2 import QtWidgets, QtCore
except:
    from PyQt5 import QtWidgets, QtCore



class CollectionView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CollectionView, self).__init__(parent)

        layout = QtWidgets.QHBoxLayout()

        #self.label = QtWidgets.QLabel()
        self.labels = []

        layout.addSpacing(1)
        #layout.addWidget(self.label)
        layout.addSpacing(1)

        self.setLayout(layout)

    def populate(self, items):
        #self.label.clear()
        for label in self.labels:
            label.clear()
            self.layout().removeWidget(label)
        self.labels.clear()

        child_count = items.children()
        if child_count == 0:
            return

        # file_size = 0
        #
        # for i in range(child_count):
        #     subitem = items.get_child(i)
        #     meta = subitem.get_info()
        #
        #     if "file_size" in meta:
        #         file_size += meta["file_size"]
        #
        # self.label.setText("Total Size: %d" % file_size)

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


        print(integer_values)





