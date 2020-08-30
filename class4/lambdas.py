from functools import partial


def val(a):
    return int(a)

a = ["100", "4", "11", "2", "15", "6"]

for i in sorted(a, key=val):
    print(i)

for i in sorted(a, key=lambda v: int(v)):
    print(i)


print(lambda v: int(v))


