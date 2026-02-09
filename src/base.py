class Shape:
    def __init__(self, type):
        self.type = type

    def in_out(self, point):
        # Placeholder method for point-in-primitive test
        raise NotImplementedError("in_out method not implemented")

class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def as_list(self):
        return [self.r, self.g, self.b]

class BaseScene:
    def __init__(self, name):
        self.name = name
        self.primitives = list()
        self.colors = list()
        self.background = Color(0, 0, 0)

    def display(self):
        print(f"Scene: {self.name}")

    def add(self, primitive, color):
        self.primitives.append(primitive)
        self.colors.append(color)

    # add iterator support for primitives zip and colors
    def __iter__(self):
        return iter(zip(self.primitives, self.colors))

