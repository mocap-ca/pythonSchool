""" This class suggests an object name (its current name + suffix) based on its type. If the object name already
contains the correct suffix, it returns the name as is. """
import re

class NewNameOperations:
    def __init__(self):
        self.suffix = ""
        self.desired_names_list = []
        self.error_message = "Not defined"

    def suggest_name(self, object_name, category_name):
        """ Adds an appropriate suffix to the object name (if there isn't one already), and returns it as the
        suggested name. Eg: The suffix '_geo' is added to a mesh object.
        :param object_name : The default text to be displayed to the user in the "New name" column.
        :type object_name : String
        :param category_name : Type of the object. Eg: mesh, joint, locator.
        :type category_name : String """
        self.suffix = "_" + category_name.lower()[:3]
        if category_name == "mesh":
            self.suffix = "_geo"
        elif category_name == "joint":
            self.suffix = "_jnt"
        elif category_name == "nurbsCurve":
            self.suffix = "_crv"
        elif category_name == "locator":
            self.suffix = "_loc"
        elif category_name == "light":
            self.suffix = "_lgt"
        elif category_name == "group":
            self.suffix = "_grp"

        if not object_name.endswith(self.suffix):
            object_name += self.suffix
        return str(object_name)

    def check_for_errors(self):
        """ Checks the new name entry for errors:
        1. If new name textbox is left empty
        2. If there is a space, replaces it with underscore
        3. If there are any special characters (other than underscore)
        4. If there are any duplicate object names
        In case of error, adds an appropriate error message, and returns True. Else, returns False"""
        if "" in self.desired_names_list:
            self.error_message = "Error: New name invalid."
            return True
        for name_index, name in enumerate(self.desired_names_list):
            if " " in name:
                name = name.replace(" ", "_")
                self.desired_names_list[name_index] = name
            if re.findall('[^A-Za-z0-9]+', name.replace("_", "")):
                self.error_message = "Error: Special characters (other than underscore) not allowed."
                return True
        if len(self.desired_names_list) != len(set(self.desired_names_list)):
            self.error_message = "Error: Duplicate names."
            return True
        return False
