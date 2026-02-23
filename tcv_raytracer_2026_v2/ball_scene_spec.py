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
            fov=60,
            img_width=800,
            img_height=600
        )
        self.lights = [
            # add a point light
            PointLight(position=Vector3D(0, 1, 1)*10, color=Color(1, 1, 1), intensity=2.6),
            # AreaLight(
            #     position=Vector3D(0, 1, 1)*10,
            #     look_at=Vector3D(0, 0, 0),
            #     up=Vector3D(0, 0, 1),
            #     width=4,
            #     height=4,
            #     color=Color(1, 1, 1),
            #     intensity=1.6
            # )
        ]

        # for i, e in enumerate([8, 16, 64, 128, 256]):
        for i, e in enumerate([.1, .2, .4, .5, .8]):
            angle = i * (math.pi / 2.5)
            # add a red specular ball
            red_material = ColorMaterial(
                diffuse_color=Color(0.5, 0, 0),
            )
            # red_material = SimpleMaterial(
            #     ambient_coefficient=0.5,
            #     diffuse_coefficient=0.2,
            #     diffuse_color=Color(0.5, 0, 0),
            #     # specular_coefficient=0,
            #     specular_coefficient=0.1,
            #     specular_color=Color(1, 1, 1),
            #     specular_shininess=e
            # )
            red_material = TranslucidMaterial(
                ambient_coefficient=0.05,
                diffuse_coefficient=0.02,
                diffuse_color=Color(0.5, 0, 0),
                specular_coefficient=0.02,
                specular_color=Color(1, 1, 1),
                specular_shininess=32,
                transmission_coefficient=0.9,
                refraction_index=1 + e  # vary refraction index for testing
            )
        
            self.add(
                Ball(center=Vector3D(0, 2*(i-2), 1.2), radius=0.95), 
                red_material
            )

        gray_material = CheckerboardMaterial(
            ambient_coefficient=1,
            diffuse_coefficient=0.8,
            square_size=1.0,
            white_color=Color(0.9, 0.9, 0.9),
            black_color=Color(0.2, 0.2, 0.2)
        )
        # gray_material = SimpleMaterial(
        # gray_material = SimpleMaterialWithShadows(
        #     ambient_coefficient=0.5,
        #     diffuse_coefficient=0.8,
        #     diffuse_color=Color(0.8, 0.8, 0.8),
        #     specular_coefficient=0,
        #     specular_color=Color(1, 1, 1),
        #     specular_shininess=32
        # )
        # gray_material = ColorMaterial(
        #     diffuse_color=Color(0.8, 0.8, 0.8)
        # )
        self.add(PlaneUV(point=Vector3D(0, 0, 0), normal=Vector3D(0, 0, 1), forward_direction=Vector3D(1, 1, 0)), gray_material)