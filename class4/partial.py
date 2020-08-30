from functools import partial


def func1(arg1, arg2):
    print("Arg1 is: %s   Arg2 is: %s" % (arg1, arg2))


x = partial(func1, "TEST")

x()



