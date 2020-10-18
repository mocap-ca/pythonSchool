This is a tool to rename the selected objects in Maya.
The tool interface, which is a pop-up window, will contain two columns: one with a list of the selected objects, sorted by object type; and the other, with a list of textboxes where the user can type the desired new name.
The second column is populated with suggestions, based on the object type, and the user can edit it.

The logic is pretty straight forward. The only point to note, is that objects such as polygons and locators contain two nodes: a transform node and a shape node. The shape node is listed as a child of the transform node. In order to find out the type of the objects, we need to access the shape node. The renaming, however, must be done to its transform node.


Here's a screenshot of the tool:

![Renamer tool screenshot](https://github.com/megmugur/MegsCodeGallery/blob/master/PyMelProjects/ObjectRenamerTool/RenamerScreenshot.jpg)