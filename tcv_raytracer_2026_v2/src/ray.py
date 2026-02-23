class Ray:
    def __init__(self, origin, direction, depth=0):
        self.origin = origin
        self.direction = direction.normalize()
        self.depth = depth  # for recursion depth if needed

    def point_at_parameter(self, t):
        return self.origin + self.direction * t