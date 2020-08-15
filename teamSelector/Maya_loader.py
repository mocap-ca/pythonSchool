import sys
sys.path.append("/Users/dan/PycharmProjects/pythonSchool/teamSelector")

from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
import teamSelector_main
from PySide2 import QtWidgets

reload(teamSelector_main)

ptr = omui.MQtUtil.mainWindow()
widget = wrapInstance(long(ptr), QtWidgets.QWidget)


d = teamSelector_main.ssDialog(widget)
d.exec_()