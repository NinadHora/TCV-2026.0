from .ray import Ray
from .camera import Camera
from .vector3d import Vector3D

CastEpsilon = 1e-4

class Shape:
    def __init__(self, type):
        self.type = type

    def hit(self, ray):
        # Placeholder method for point-in-primitive test
        raise NotImplementedError("in_out method not implemented")

class Color(Vector3D):
    def __init__(self, r, g, b):
        super().__init__(r, g, b)

    @property
    def r(self):
        return self.x
    @property
    def g(self):
        return self.y
    @property
    def b(self):
        return self.z

    def clamp(self, min_value=0.0, max_value=1.0):
        self.x = max(min(self.x, max_value), min_value)
        self.y = max(min(self.y, max_value), min_value)
        self.z = max(min(self.z, max_value), min_value)

    def as_list(self):
        return [self.x, self.y, self.z]

class BaseScene:
    def __init__(self, name):
        self.name = name
        self.shapes = list()
        self.materials = list()
        # default background color and camera
        self.background = Color(0, 0, 0)
        # ambient light
        self.ambient_light = Color(0.1, 0.1, 0.1)

        self.camera = Camera(
            eye=Vector3D(0, 0, 5),
            look_at=Vector3D(0, 0, 0),
            up=Vector3D(0, 1, 0),
            fov=45,
            img_width=800,
            img_height=600
        )

    def display(self):
        print(f"Scene: {self.name}")

    def add(self, primitive, material):
        self.shapes.append(primitive)
        self.materials.append(material)

    # add iterator support for primitives zip and colors
    def __iter__(self):
        return iter(zip(self.shapes, self.materials))
    def hit(self, ray):
        # check for hits with all shapes
        hit_rec = HitRecord()
        for shape, material in zip(self.shapes, self.materials):
            new_hit = shape.hit(ray)
            if new_hit.hit and new_hit.t < hit_rec.t and new_hit.t > CastEpsilon:
                hit_rec = new_hit
                # set material
                hit_rec.material = material
                hit_rec.ray = ray
        return hit_rec

class HitRecord:
    def __init__(self, hit=False, t=float('inf'), point=None, normal=None, material=None, ray=None, uv=None):
        self.hit = hit
        self.t = t
        self.point = point
        self.normal = normal
        self.material = material
        self.ray = ray
        self.uv = uv

class Material:
    def __init__(self):
        pass

    def shade(self, hit_record, scene):
        # Placeholder method for shading
        raise NotImplementedError("shade method not implemented")