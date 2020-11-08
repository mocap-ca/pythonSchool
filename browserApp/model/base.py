class BaseItem(object):

    def __init__(self):
        pass

    def update(self):
        """ Repopulates the data in the item from the source """
        return NotImplementedError

    def short_name(self):
        """ Returns the short name for use in the ui, e.g. the tree """
        return NotImplementedError

    def children(self):
        """ Returns an integer for the number of children under this node, or 0 if there are no children """
        return NotImplementedError

    def get_child(self, n):
        """ returns the child at location n as a BaseItem object """

    def get_icon(self):
        """ returns the name of the icon file to use for this object, or None if an icon is not set """
        return None

    def get_info(self):
        """ returns a dict of information about the item """
        return NotImplementedError

    def actions(self):
        """ returns a list of actions that can be performed """
        return NotImplementedError

    def perform_action(self, name):
        """ perform an action """
        return NotImplementedError

