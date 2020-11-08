from browserApp.model.base import BaseItem
import os
from datetime import datetime

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

    def format_time(self, time_value):
        '''Function for formating time'''
        return datetime.fromtimestamp(time_value).strftime('%Y-%b-%d %H:%M')

    def get_info(self):
        data = {
            'full_path': self.full_path,
        }

        if os.path.isfile(self.full_path):
            stat = os.stat(self.full_path)
            print(stat.st_ctime)
            data['Type'] = os.path.splitext(self.full_path)[1] # Get extension from filename
            data['file_name: '] = os.path.splitext(self.full_path)[0] # Get filename
            data['file_size'] = os.path.getsize(self.full_path) # store the file size in "12.23MB" format
            data['created'] = self.format_time(stat.st_ctime)
            data['modified'] = self.format_time(stat.st_mtime)
            #data['device'] = str(stat.st_dev)



        if os.path.isdir(self.full_path):
            data['type'] = "Dir"

        return data



