
class Foo(object):
    def __str__(self):
        return "Foo!"
    pass


class Bloop():

    def __init__(self, value):
        self.value = value

    def __str__(self):
        ret = "I am a bloop, my value is: "
        if isinstance(self.value, float):
            return ret + "%.04f" % self.value
        if isinstance(self.value, int):
            return ret + "%d" % self.value

        return ret + " string value of: " + str(self.value)


items = [ "Apple", 0.4,  2, "Carrot",  Foo,  Foo() ]


for i in items:
    print(str(i))





