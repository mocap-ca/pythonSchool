class HumbleThings:
        def __init__(self):
            print("\nThis is the greatest print statement ever. Why? Bcoz, you know..logic.\n")

        def without_lambda(self):
            x = 2
            y = 3
            return x + y

        def with_lambda(self):
            return (lambda x, y: x + y)(2, 3)

one_object = HumbleThings()

print(one_object.with_lambda())
print(one_object.without_lambda())



