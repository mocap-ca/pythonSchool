""" This is a program to rename selected objects in Maya. The pop-up window will contain two columns:
one with a list of the selected objects, sorted by object type;
and the other, with a list of textboxes where the user can type the desired new name.
The second column is populated with suggestions, based on the object type, and the user can edit it.

TODO: Add reload button on top to refresh and modify selection while window is still open
TODO: Check more case types
TODO: Add check-boxes to ask user if modifying suffix for one object should automatically modify the suffixes for all
objects of its type. """
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance

from PySide2 import QtWidgets, QtCore
import pymel.core as pm
import os


class RenamerDialog(QtWidgets.QDialog):
    def __init__(self):
        """ The initialization includes setting up the UI framework for the tool window, ensuring that the selection is
        not empty, and calling the method that populates the form with relevant data. """
        ptr = omui.MQtUtil.mainWindow()
        parent = wrapInstance(long(ptr), QtWidgets.QWidget)
        super(RenamerDialog, self).__init__(parent)

        self.setWindowTitle("Object Renamer")
        self.main_layout = QtWidgets.QGridLayout()
        self.main_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(self.main_layout)

        self.setFixedSize(520, 620)

        empty_selection = self.no_selection_check()
        if empty_selection:
            return
        self.populate_window()

    def no_selection_check(self):
        """ This method checks if selection is empty. If empty, it creates an error label and returns True.
        Else, returns false.
        :return bool : True if selection is empty
        :type bool : Boolean """
        if not pm.ls(dag=True, sl=True):
            no_selection_label = QtWidgets.QLabel("Nothing selected")
            self.main_layout.addWidget(no_selection_label)
            return True
        return False

    def populate_window(self):
        """ Calls the methods that populate: the 'from' and 'to' labels on top, the 'rename and close' button at the
        bottom, and the objects lists in the middle. """
        self.display_labels_and_buttons()
        self.create_lists()
        self.display_lists()

    def display_labels_and_buttons(self):
        """Creates the 'Current name' and 'New name' headings on top, and the 'rename and close' button at the bottom.
        Sets up the signal-slot connection for the button. ie, on button press, calls the rename_objects() method."""
        self.display_to_and_from()

        self.button = QtWidgets.QPushButton("Rename and close")
        self.button.pressed.connect(self.rename_objects)

        self.main_layout.addWidget(self.button, 2, 0)

    def display_to_and_from(self):
        """Creates the labels for 'Current name' and 'New name' list-headings, puts them in a QHBox layout,
        and adds them to the pop-up UI"""
        self.heading_bar = QtWidgets.QWidget()
        self.heading_bar_layout = QtWidgets.QHBoxLayout()
        self.heading_bar.setLayout(self.heading_bar_layout)

        self.from_label = QtWidgets.QLabel("Current name:")
        self.to_label = QtWidgets.QLabel("New Name:")
        self.heading_bar_layout.addWidget(self.from_label)
        self.heading_bar_layout.addWidget(self.to_label)

        self.main_layout.addWidget(self.heading_bar)

    def create_lists(self):
        """Calls the methods that create:
        1. A list of Shape objects.
        2. A dictionary with objects as values, and their types as keys."""
        self.create_shapeobjects_list()
        self.create_objects_dictionary()

    def create_shapeobjects_list(self):
        """Creates a list of Shape objects from the selection."""
        self.shape_objects_list = []
        for each_object in pm.ls(dag=True, sl=True):
            if each_object.listRelatives(shapes=True):
                shape_object = each_object.getShape()
                self.shape_objects_list.append(shape_object)

    def create_objects_dictionary(self):
        """Creates a dictionary with objects as values, and their types as keys.
        Looks at every object in the selection.
        If it is a shape node, does not add it to the dictionary. This is because Maya will automatically update the
        name of the shape node, when we modify the name of the transform node.
        If it is a transform node, gets the type of the object by accessing its Shape node, and adds it to that category
        in t he dictionary.
        If it a transform node without a shape node, gives a suggestion that it could be a group object.

         """
        self.objects_dictionary = {}
        for selected_object in pm.ls(dag=True, sl=True):
            if selected_object in self.shape_objects_list:  # when it is a shape node
                continue
            elif selected_object.listRelatives(shapes=True):  # when it contains a shape node
                shape_object = selected_object.getShape()
                object_type = pm.objectType(shape_object)
            elif pm.objectType(selected_object) == "transform":
                object_type = "group"                      # when it contains a transform node but no shape node
            else:                                          # when not a shape node, and doesn't contain one
                object_type = pm.objectType(selected_object)
            if object_type not in self.objects_dictionary:
                self.objects_dictionary[object_type] = []
            self.objects_dictionary[object_type].append(selected_object)

    def display_lists(self):
        """Sets up the UI elements for the 'Current name' and 'New name' lists.
        Adds a scroll for the lists."""
        self.scroll_area_widget = QtWidgets.QScrollArea()
        self.set_scroll_area_style()

        self.list_grid_layout = QtWidgets.QGridLayout()
        self.list_widget = QtWidgets.QWidget()
        self.list_widget.setLayout(self.list_grid_layout)
        self.list_grid_layout.setAlignment(QtCore.Qt.AlignTop)

        self.populate_list_grid_layout()

        self.scroll_area_widget.setWidget(self.list_widget)
        self.main_layout.addWidget(self.scroll_area_widget, 1, 0)

    def set_scroll_area_style(self):
        """Sets up the style for the scrollable area containing the lists."""
        self.scroll_area_widget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.scroll_area_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area_widget.setWidgetResizable(True)

    def populate_list_grid_layout(self):
        """The scroll area contains a list of categories(object types). Each of these categories contains a QGridLayout,
        with all the objects of that type, listed under it.
        A new dictionary is created, which will hold: the object names as keys, and name of the textbox that contains
        its new name as the value. This mapping will help with the renaming action, on button press."""
        row_index = 0
        self.new_name_dictionary = {}

        for object_type, objects_list in self.objects_dictionary.items():
            type_name = str(object_type).capitalize() + " objects:"
            category_label = QtWidgets.QLabel(type_name)
            self.list_grid_layout.addWidget(category_label, row_index, 0)
            row_index += 1

            # Create a new category widget (Eg. for Mesh objects, Locator objects)
            category_wise_grid = QtWidgets.QWidget()
            self.category_wise_grid_layout = QtWidgets.QGridLayout()
            self.category_wise_grid_layout.setHorizontalSpacing(0)
            self.category_wise_grid_layout.setVerticalSpacing(0)

            # Obtain a list of all objects of the category type
            self.populate_each_category(objects_list, object_type)

            # Add the category along with its list to the display
            category_wise_grid.setLayout(self.category_wise_grid_layout)
            self.list_grid_layout.addWidget(category_wise_grid, row_index, 0)
            row_index += 1

    def populate_each_category(self, all_objects_in_category, category):
        """ For each object in the list, creates two textboxes: one for the current name, and one for the desired new
        name. Adds these textboxes to the layout. The current names have to be non-editable.
        :param all_objects_in_category : List of all objects of the same type. Eg: All locator objects.
        :type all_objects_in_category : List
        :param category : Type of the objects in the list
        :type category : Object type
        """
        object_index = 0
        for each_object in all_objects_in_category:
            suggested_name = self.suggest_name(each_object, category)

            from_textbox = QtWidgets.QLineEdit(str(each_object))
            to_textbox = QtWidgets.QLineEdit(suggested_name)
            from_textbox.setEnabled(False)

            self.new_name_dictionary[each_object] = to_textbox
            self.category_wise_grid_layout.addWidget(from_textbox, object_index, 0)
            self.category_wise_grid_layout.addWidget(to_textbox, object_index, 1)
            object_index += 1

    def suggest_name(self, suggested_name, category_name):
        """ Adds an appropriate suffix to the object name (if there isn't one already), and returns it as the
        suggested name. Eg: The suffix '_geo' is added to a mesh object.
        :param suggested_name : The default text to be displayed to the user in the "New name" column.
        :type suggested_name : String
        :param category_name : Type of the object. Eg: mesh, joint, locator.
        :type category_name : String """
        if category_name == "mesh":
            suffix = "_geo"
        elif category_name == "joint":
            suffix = "_jnt"
        elif category_name == "nurbsCurve":
            suffix = "_crv"
        elif category_name == "locator":
            suffix = "_loc"
        elif category_name == "group":
            suffix = "_grp"
        else:
            suffix = "_" + category_name.lower()[:3]

        if not suggested_name.endswith(suffix):
            suggested_name += suffix
        return str(suggested_name)

    def rename_objects(self):
        """ This method goes through the key-value pairs in the new_name_dictionary, and renames the objects in Maya,
        based on the content of the corresponding textboxes.
        The new_name_dictionary contains: the object names as keys,
        and names of the corresponding textboxes (which in turn, contain the desired new names) as the values. """
        for every_object, corresponding_textbox in self.new_name_dictionary.items():
            pm.rename(every_object, str(corresponding_textbox.text()))
        self.close()


INSTANCE = None
def show_gui():
    """ Singleton to create the gui if it doesn't exist, or show if it does """
    global INSTANCE
    if not INSTANCE:
        INSTANCE = RenamerDialog()
    INSTANCE.show()
    return INSTANCE