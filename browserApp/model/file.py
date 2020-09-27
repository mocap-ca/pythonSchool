from browserApp.model.base import BaseItem
import os


class FileItem(BaseItem):
    def __init__(self, full_path):
        super(FileItem, self).__init__()
        self.full_path = full_path
        self.file_list = None

    def update(self):
        """ Populates self.file list - sets to empty list if no items were found """
        if os.path.isdir(self.full_path):
            self.file_list = os.listdir(self.full_path)
        else:
            self.file_list = []

    def short_name(self):
        return os.path.split(self.full_path)[1]

    def children(self):
        if self.file_list is None:
            self.update()

        # ASSERT
        if self.file_list is None:
            raise RuntimeError("Invalid file list while finding children")

        return len(self.file_list)

    def get_child(self, n):
        if self.file_list is None:
            self.update()

        # ASSERT
        if self.file_list is None:
            raise RuntimeError("Invalid file list while getting children")

        return FileItem(os.path.join(self.full_path, self.file_list[n]))

    def get_info(self):
        data = {
            'full_path': self.full_path,
        }

        if os.path.isfile(self.full_path):
            stat = os.stat(self.full_path)
            data['type'] = "File"
            data['file_size'] = str(stat.st_size)
            data['created'] = str(stat.st_ctime)

        if os.path.isdir(self.full_path):
            data['type'] = "Dir"

        return data



