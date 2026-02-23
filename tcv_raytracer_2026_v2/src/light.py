from random import uniform
from .vector3d import Vector3D
from .base import Color

class Light:
    def __init__(self):
        pass

    def position(self):
        raise NotImplementedError("Subclasses should implement this method")
class PointLight:
    def __init__(self, position: Vector3D, color: Color, intensity: float = 1.0):
        self.pos = position  # position is a Vector3
        self.color = color  # color is a Color
        self.intensity = intensity  # intensity is a float

    def position(self):
        return self.pos

class AreaLight:
    def __init__(self, position, look_at, up, width, height, color=Color(1, 1, 1), intensity=1.0):
        self.pos = position
        self.color = color
        self.intensity = intensity
        self.w = (position - look_at).normalize()
        self.su = width
        self.sv = height
        up = up.normalize()
        self.u = up.cross(self.w).normalize()
        self.v = self.w.cross(self.u).normalize()

    def position(self):
        # from image coordinates to coordinates 
        # in the camera's view plane
        u, v = uniform(0, 1), uniform(0, 1)
        x = self.su * u - self.su / 2
        y = self.sv * v - self.sv / 2

        # from view plane to world coordinates
        return self.pos + self.u * x + self.v * y