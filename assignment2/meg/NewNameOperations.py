""" This class suggests an object name (its current name + suffix) based on its type. If the object name already
contains the correct suffix, it returns the name as is. """
import re
import os
import json

def validate_desired_names(desired_names_list):
    """ Checks the new name entry for errors:
    1. If new name textbox is left empty
    2. If there is a space : replaces it with underscore
    3. If there are any special characters (other than underscore)
    4. If there are any duplicate object names
    In case of error, adds an appropriate error message, and returns True. Else, returns False"""
    error_message = None
    if "" in desired_names_list:
        error_message = "Error: New name invalid."
        return error_message
    for name_index, name in enumerate(desired_names_list):
        if " " in name:
            name = name.replace(" ", "_")
            desired_names_list[name_index] = name
        if re.findall('[^A-Za-z0-9]+', name.replace("_", "")):
            error_message = "Error: Special characters (other than underscore) not allowed."
            return error_message
    if len(desired_names_list) != len(set(desired_names_list)):
        error_message = "Error: Duplicate names."

    return error_message


def suggest_name(object_name, category_name):
    """ Adds an appropriate suffix to the object name (if there isn't one already), and returns it as the
    suggested name. Eg: The suffix '_geo' is added to a mesh object.
    :param object_name : Name of the object that needs renaming
    :type object_name : String
    :param category_name : Type of the object. Eg: mesh, joint, locator.
    :type category_name : String
    :return object_name : A name suggestion, with a suffix added to the object name(if no error). Suffix is based on
    the object_type.
    :rtype object_name : String """

    suffix = "_" + category_name.lower()[:3]
    directory_path = "Database\SuffixDatabase.json"
    suffix_dict = None

    if not os.path.isfile(directory_path) or not os.access(directory_path, os.R_OK):  # case: data loading failed.
        print("Error: Directory not found or not readable")
        return object_name
    database_file = open(directory_path)

    try:  # case: data loading successful.
        suffix_dict = json.load(database_file)
        if category_name in suffix_dict:
            suffix = suffix_dict[category_name]
    except ValueError as json_error:
        print("Error: ", str(json_error))
    if not suffix_dict:
        print("Error: Suffixes database is empty")

    if not object_name.endswith(suffix):
        object_name += suffix
    return object_name
