

class Foo(object):

    def __init__(self):
        self.bar = None

    def whatAnimal(self):
        raise NotImplementedError

    def makeSound(self):
        animal = self.whatAnimal()

        if animal == "Sheep":
            print("Baaaa!")
            return

        print("invalid animal: " + str(animal))


class FooSheep(Foo):
    def __init__(self):
        super(FooSheep, self).__init__()


    def whatAnimal(self):
        return "Sheep"



if __name__ == "__main__":

    f = FooSheep()
    f.makeSound()

