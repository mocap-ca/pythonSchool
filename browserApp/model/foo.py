
import browserApp.model.file as bmf
import browserApp.model.stub as bms

import os


def filetest(f_path):
    for i in os.listdir(f_path):
        full_path = os.path.join(f_path, i)
        item = bmf.FileItem(full_path)
        print(item.full_path)
        print("% 6d %s    %s" % (item.children(), item.get_info(), str(item.get_icon())))


def stubtest():
    for i in range(10):
        item = bms.StubItem(3)
        print("% 6d %s" % (item.children(), item.short_name()))


if __name__ == "__main__":
    path = input("Type in path: ")
    #stubtest()
    filetest(path)

