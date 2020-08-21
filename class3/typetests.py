

def sortfunc(a):
    return a.bloop






class Foo():
    def __init__(self, value):
        self.bloop = value

    def __str__(self):
        return "Bloop is: %d" % self.bloop




def printme(thingy):
    a = Foo(1234)
    ret = thingy(a)

    print("You gave me: " + str(ret))

printme(lambda v: v.bloop)


a = [ Foo(20), Foo(1), Foo(99), Foo(5), Foo(8), Foo(6) ]


myFoo = Foo(1001)

test = lambda v: v.bloop

