""" This will show detailed information about an item """

from PyQt5 import QtWidgets


class CollectionView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CollectionView, self).__init__(parent)

        layout = QtWidgets.QHBoxLayout()

        self.label = QtWidgets.QLabel()
        self.label.setText("Collection")

        layout.addSpacing(1)
        layout.addWidget(self.label)
        layout.addSpacing(1)

        self.setLayout(layout)

    def populate(self, items):
        self.label.setText("")
        child_count = items.children()
        if child_count == 0:
            return

        file_size = 0

        for i in range(child_count):
            subitem = items.get_child(i)
            meta = subitem.get_info()

            if "file_size" in meta:
                file_size += meta["file_size"]

        self.label.setText("Total Size: %d" % file_size)

        # keys = set()
        #
        # integer_values = {}
        #
        # for i in range(child_count):
        #     subitem = items.get_child(i)
        #     meta = subitem.get_info()
        #     keys.update(meta.keys())
        #
        # for i in range(child_count):
        #     subitem = items.get_child(i)
        #     meta = subitem.get_info()
        #
        #     for key in keys:
        #         value = meta[key]
        #         if isinstance(value, int):
        #             if key not in integer_values:
        #                 integer_values[key] = 0
        #             integer_values[key] += value
        #
        #
        # print(integer_values)





