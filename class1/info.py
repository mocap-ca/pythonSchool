import sys
class Foo(object):
    """ Foo is a useful class for fooing things. """

    def __init__(self):
        """ Sets self.value as None """
        self.value = None

    def add_one(self):
        """ Increments the internal counter by one, while the socket conditions remain valid """
        pass

    def blah(self, value1, value2):
        """
        The main text goes here
        """
        return str(value1) + str(value2)

    def __str__(self):
        print("Hello!")


for i in dir(Foo):
    print(i)
