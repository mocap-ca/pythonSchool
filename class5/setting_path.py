import sys

"""
import sys
#sys.path.append("/Users/alastairmacleod/git/github/pythonSchool/")   

import class5.setting_path as sp

sp.print_paths()


Setting via maya.env...
 /Users/alastairmacleod/Library/Preferences/Autodesk/maya/2020
 /Documents/maya/2020/Maya.env
 
add this line:

PYTHONPATH=/Users/alastairmacleod/git/github/pythonSchool/
   
"""

def print_paths():
    for i in sys.path:
        print(i)


if __name__ == "__main__":
    print_paths()