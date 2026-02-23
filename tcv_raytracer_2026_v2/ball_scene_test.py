# defines a scene with a ball using implicit function
import math
from src.base import BaseScene, Color
from src.shapes import Ball, PlaneUV
from src.camera import Camera
from src.vector3d import Vector3D
from src.light import PointLight, AreaLight
from src.materials import ColorMaterial, SimpleMaterial, SimpleMaterialWithShadows, TranslucidMaterial, CheckerboardMaterial

# class name should be Scene
class Scene(BaseScene):
    def __init__(self):
        super().__init__("Ball Scene")

        # light blue background
        self.background = Color(0.7, 0.8, 1)
        self.ambient_light = Color(0.1, 0.1, 0.1)
        self.max_depth = 10  # for reflections/refractions
        self.camera = Camera(
            eye=Vector3D(1, 0, .3)*10.0,
            look_at=Vector3D(0, 0, 1.8),
            up=Vector3D(0, 0, 1),
            fov=30,
            img_width=800,
            img_height=600
        )
        self.lights = [
            # add a point light
            # PointLight(position=Vector3D(0, 1, 1)*10, color=Color(1, 1, 1), intensity=1.6),
            AreaLight(
                position=Vector3D(0, 1, 1)*10,
                look_at=Vector3D(0, 0, 0),
                up=Vector3D(0, 0, 1),
                width=4,
                height=4,
                color=Color(1, 1, 1),
                intensity=1.6
            )
        ]

        # add a red translucent ball
        red_material = TranslucidMaterial(
            ambient_coefficient=0.05,
            diffuse_coefficient=0.02,
            diffuse_color=Color(0.5, 0, 0),
            specular_coefficient=0.02,
            specular_color=Color(1, 1, 1),
            specular_shininess=32,
            transmission_coefficient=0.8,
            refraction_index=1.5
        )
        # red_material = ColorMaterial(
        #     diffuse_color=Color(0.5, 0, 0),
        # )
        # red_material = SimpleMaterial(
        #     ambient_coefficient=0.5,
        #     diffuse_coefficient=0.2,
        #     diffuse_color=Color(0.5, 0, 0),
        #     # specular_coefficient=0,
        #     specular_coefficient=0.1,
        #     specular_color=Color(1, 1, 1),
        #     specular_shininess=32
        # )
        
        self.add(
            Ball(center=Vector3D(0, 0, 1.2), radius=1), 
            red_material
        )

        # blue ball
        blue_material = SimpleMaterial(
            ambient_coefficient=0.5,
            diffuse_coefficient=0.2,
            diffuse_color=Color(0, 0, 0.5),
            specular_coefficient=0.5,
            # specular_coefficient=0,
            specular_color=Color(1, 1, 0),
            specular_shininess=32
        )
        # blue_material = ColorMaterial(
        #     diffuse_color=Color(0, 0, 0.5),
        # )
        d = 2.2
        self.add(
            Ball(center=Vector3D(-d, -d/2, math.sqrt(2)), radius=math.sqrt(2)), 
            blue_material
        )

        # ground plane
        # gray_material = CheckerboardMaterial(
        #     ambient_coefficient=1,
        #     diffuse_coefficient=0.8,
        #     square_size=1.0,
        #     white_color=Color(0.9, 0.9, 0.9),
        #     black_color=Color(0.2, 0.2, 0.2)
        # )
        # gray_material = SimpleMaterial(
        gray_material = SimpleMaterialWithShadows(
            ambient_coefficient=0.5,
            diffuse_coefficient=0.8,
            diffuse_color=Color(0.8, 0.8, 0.8),
            specular_coefficient=0,
            specular_color=Color(1, 1, 1),
            specular_shininess=32
        )
        # gray_material = ColorMaterial(
        #     diffuse_color=Color(0.8, 0.8, 0.8)
        # )
        self.add(PlaneUV(point=Vector3D(0, 0, 0), normal=Vector3D(0, 0, 1), forward_direction=Vector3D(1, 1, 0)), gray_material)