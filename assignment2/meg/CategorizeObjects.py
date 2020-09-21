"""
Class sorts the list of objects into categories based on the types of the objects in the list.
"""
import os
import pymel.core as pm
import pprint

class CategorizeObjects:
    def __init__(self):
        self.objects_list = []
        self.shape_objects_list = []
        self.objects_dictionary = {}

    def create_object_containers(self):
        """Calls the methods that create:
        1. A list of Shape objects.
        2. A dictionary with object names as values, and their types as keys."""
        self.create_shape_objects_list()
        self.create_objects_dictionary()

    def create_shape_objects_list(self):
        """Creates a list of Shape objects from the selection."""
        for each_object in self.objects_list:
            if each_object.listRelatives(shapes=True):
                shape_object = each_object.getShape()
                self.shape_objects_list.append(shape_object)

    def create_objects_dictionary(self):
        """Populates the dictionary with objects as values, and their types as keys. """
        for selected_object in self.objects_list:
            if selected_object in self.shape_objects_list:  # if it is a shape node, do not add to dictionary
                continue
            elif selected_object.listRelatives(shapes=True):  # if it has a shape node as a child,
                shape_object = selected_object.getShape()     # get its type by accessing the shape node.
                object_type = pm.objectType(shape_object)
            elif pm.objectType(selected_object) == "transform":
                object_type = "group"              # if it contains a transform node but no shape node, could be a group
            else:
                object_type = pm.objectType(selected_object)  # else, find it's type
            if object_type not in self.objects_dictionary:  # if category is not already a key in the dictionary, add it
                self.objects_dictionary[object_type] = []
            self.objects_dictionary[object_type].append(selected_object)  # add the object to the dictionary


