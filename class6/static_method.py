

class Test(object):
    def __init__(self, x):
        self.x = x
        pass

    def foo(self, arg):
        self.x = arg

    @staticmethod
    def create123():
        x = Test('123')
        return x

    def __str__(self):
        return str(self.x)


def create123():
    y = Test('345')
    return y

if __name__ == "__main__":

    obj = create123()

    print(obj)