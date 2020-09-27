from browserApp.model.base import BaseItem


class StubItem(BaseItem):
    def __init__(self, child_count=0):
        super(StubItem, self).__init__()
        self.child_count = child_count

    def short_name(self):
        return "STUB"

    def children(self):
        return self.child_count

    def get_child(self, n):
        if n == 0:
            return StubItem(1)
        if n == 1:
            return StubItem(4)

        return StubItem()

    def get_icon(self):
        return "stub.png"

    def get_info(self):
        return {'Stub': "Stub", "Animal": "Sheep", "Sound": "Baaaaa"}

