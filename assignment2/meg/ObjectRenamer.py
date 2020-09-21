""" This is a program to rename selected objects in Maya. The pop-up window will contain:
a list of the selected objects, sorted by their types,
and a textbox next to each object, for the user to type the desired new name.
The textbox is populated with suggestions, based on the object type, and the user can edit it.
TODO - Future enhancements:
1. indicate which textbox needs editing, to fix the displayed error.
2. When user hits Undo once after using the tool, the entire list of names should be reverted at once.
3. Check more test cases
4. Add reload button to reload (possibly new) selection while window is still open
5. Add check-boxes to ask user if modifying suffix for one object should similarly modify suffixes for all
objects of that category. """

import pymel.core as pm
from PySide2 import QtWidgets, QtCore
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance

import CategorizeObjects
import NewNameOperations

class RenamerDialog(QtWidgets.QDialog):
    def __init__(self):
        """ The initialization includes setting up the UI framework for the tool window, and calling the method
         which will do an initial check and start setting up the window."""
        pointer = omui.MQtUtil.mainWindow()
        parent = wrapInstance(long(pointer), QtWidgets.QWidget)
        super(RenamerDialog, self).__init__(parent)

        self.setWindowTitle("Object Renamer")
        self.main_layout = QtWidgets.QGridLayout()
        self.main_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(self.main_layout)
        self.setGeometry(500, 200, 520, 620)

        self.initial_check_and_start()

    def initial_check_and_start(self):
        """This method creates a list of all selected dag objects, and checks if selection is empty.
        If it is empty, displays an error message. If not, it goes ahead, and sets up the object lists' display.
        It also creates an object of the CategorizeObjects class, and initializes variables which will be used later."""

        self.all_selected_objects = pm.ls(dagObjects=True, selection=True, dependencyNodes=True)

        if not self.all_selected_objects:
            no_selection_label = QtWidgets.QLabel("Nothing selected.")
            self.main_layout.addWidget(no_selection_label)
            return

        self.categorize_object = CategorizeObjects.CategorizeObjects()
        self.row_index = 0
        self.new_name_dictionary = {}
        self.desired_names_list = []

        self.populate_window()


    def populate_window(self):
        """ Calls the methods that create and display the UI widgets in the popup window"""
        self.initialize_ui_elements()

        # add heading labels to the top of the window
        self.setup_heading_labels()

        # create two lists (one for current object names, one for the desired new names) and add them to the display.
        self.categorize_object.objects_list = self.all_selected_objects
        self.categorize_object.create_object_containers()
        self.setup_scroll_area_widget()

        # create a rename button, and add it to the bottom of the display
        self.setup_rename_button()

    def initialize_ui_elements(self):
        """Creates all the UI elements for the dialog window, except the dynamically created ones."""
        self.scroll_area_widget = QtWidgets.QScrollArea()
        self.list_widget = QtWidgets.QWidget()
        self.list_grid_layout = QtWidgets.QGridLayout()

        self.current_name_label = QtWidgets.QLabel("Current name:")
        self.new_name_label = QtWidgets.QLabel("New Name:")
        self.heading_bar = QtWidgets.QWidget()
        self.heading_bar_layout = QtWidgets.QHBoxLayout()
        self.error_label = QtWidgets.QLabel()

        self.rename_button = QtWidgets.QPushButton("Rename and close")


    def setup_heading_labels(self):
        """ Encases the labels for 'Current name' and 'New name' list-headings in a QHBox layout, and adds
        them to the main layout. """
        self.heading_bar.setLayout(self.heading_bar_layout)
        self.heading_bar_layout.addWidget(self.current_name_label)
        self.heading_bar_layout.addWidget(self.new_name_label)
        self.main_layout.addWidget(self.heading_bar)

    def setup_rename_button(self):
        """ Makes the signal-slot connection for the 'rename and close' button at the bottom.
        i.e., on button press, calls the rename_objects() method. """
        self.rename_button.pressed.connect(self.rename_objects)
        self.main_layout.addWidget(self.rename_button, 2, 0)

    def setup_scroll_area_widget(self):
        """ Sets up the UI elements for scrollable area (the lists widget)."""
        self.setup_scroll_area_style()

        self.list_widget.setLayout(self.list_grid_layout)
        self.list_grid_layout.setAlignment(QtCore.Qt.AlignTop)

        self.populate_list_grid_layout()

        self.scroll_area_widget.setWidget(self.list_widget)
        self.main_layout.addWidget(self.scroll_area_widget, 1, 0)

    def setup_scroll_area_style(self):
        """ Sets up the style for the scrollable area containing the lists."""
        self.scroll_area_widget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.scroll_area_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll_area_widget.setWidgetResizable(True)

    def populate_list_grid_layout(self):
        """ The scroll area contains a list of categories(object types), each of which contains a QGridLayout, with all
        the objects of that type, listed under it.
        A new dictionary is created, which will hold: the object names as keys, and name of the textbox that contains
        its new name as the value. This mapping will help with the renaming action, on button press."""

        for object_type, objects_list in self.categorize_object.objects_dictionary.items():
            type_name = str(object_type).capitalize() + " objects:"
            category_label = QtWidgets.QLabel(type_name)
            self.list_grid_layout.addWidget(category_label, self.row_index, 0)
            self.row_index += 1

            # Create a new category widget (Eg. for Mesh type objects)
            category_wise_grid = QtWidgets.QWidget()

            self.category_wise_grid_layout = QtWidgets.QGridLayout()     # Dynamic creation
            self.category_wise_grid_layout.setHorizontalSpacing(0)
            self.category_wise_grid_layout.setVerticalSpacing(0)

            # Obtain a list of all objects of the category type
            self.populate_each_category(objects_list, object_type)

            # Add the category along with its list to the display
            category_wise_grid.setLayout(self.category_wise_grid_layout)
            self.list_grid_layout.addWidget(category_wise_grid, self.row_index, 0)
            self.row_index += 1
            # print(object_type, objects_list)

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
            suggested_name = NewNameOperations.suggest_name(each_object, category)
            from_textbox = QtWidgets.QLineEdit(str(each_object))
            to_textbox = QtWidgets.QLineEdit(suggested_name)
            from_textbox.setEnabled(False)

            self.new_name_dictionary[each_object] = to_textbox
            self.category_wise_grid_layout.addWidget(from_textbox, object_index, 0)
            self.category_wise_grid_layout.addWidget(to_textbox, object_index, 1)
            object_index += 1

    def rename_objects(self):
        """ This method goes through the key-value pairs in the new_name_dictionary, and renames the objects in Maya,
        based on the content of the corresponding textboxes.
        The new_name_dictionary contains: the object names as keys,
        and names of the corresponding textboxes (which in turn, contain the desired new names) as the values. """

        for every_object, corresponding_textbox in self.new_name_dictionary.items():
            self.desired_names_list.append(corresponding_textbox.text())
        error_message = NewNameOperations.validate_desired_names(self.desired_names_list)
        if error_message:
            self.error_label.setText(self.new_name_object.error_message)
            self.list_grid_layout.addWidget(self.error_label, self.row_index, 0)
            self.row_index += 1
            return
        else:
            for object_index, every_object in enumerate(self.new_name_dictionary.keys()):
                pm.rename(every_object, self.desired_names_list[object_index])
            self.close()


INSTANCE = None


def show_gui():
    """ Singleton to create the gui if it doesn't exist, or show if it does """
    global INSTANCE
    if not INSTANCE:
        INSTANCE = RenamerDialog()
    INSTANCE.show()
    return INSTANCE
