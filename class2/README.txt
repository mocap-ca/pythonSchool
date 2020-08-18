####################
# Run this in your maya script editor:

import sys

# change this path to your location of the pythonSchool git repo
sys.path.append("/Users/alastairmacleod/git/github/pythonSchool")

from class2 import mayaGui

if mayaGui.INSTANCE:
    mayaGui.INSTANCE.close()
    mayaGui.INSTANCE

reload(mayaGui)

mayaGui.show_gui()

