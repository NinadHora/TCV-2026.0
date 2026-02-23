"""
Tarefa 4 – Espelhos
Dois planos espelhados opostos, camera no meio.
O numero de reflexoes visivel e limitado por max_depth.
"""
import math
from src.base import BaseScene, Color
from src.shapes import Ball, Plane, PlaneUV, Cylinder
from src.camera import Camera
from src.vector3d import Vector3D
from src.light import PointLight, AreaLight
from src.materials import SimpleMaterialWithShadows, MirrorMaterial, CheckerboardMaterial


class Scene(BaseScene):
    def __init__(self):
        super().__init__("Task 4 – Mirrors")
        self.background    = Color(0.0, 0.0, 0.0)
        self.ambient_light = Color(0.08, 0.08, 0.08)
        self.max_depth     = 12     # <-- varie este valor!

        self.camera = Camera(
            eye     = Vector3D(0, 0, 1.5),
            look_at = Vector3D(1, 0, 1.5),   # olhando para o corredor entre espelhos
            up      = Vector3D(0, 0, 1),
            fov=60, img_width=800, img_height=600
        )

        self.lights = [
            PointLight(Vector3D(0, 3, 2.8), Color(1, 0.95, 0.8), intensity=2.0),
            PointLight(Vector3D(0, -3, 2.8), Color(0.6, 0.8, 1.0), intensity=1.2),
        ]

        mirror  = MirrorMaterial(reflectivity=0.95, tint=Color(0.95,0.95,1.0))
        mirror2 = MirrorMaterial(reflectivity=0.92, tint=Color(1.0, 0.95, 0.9))

        mat_ball = SimpleMaterialWithShadows(0.05, 0.7, Color(0.9,0.5,0.1),
                                             0.6, Color(1,1,1), 100)
        mat_floor = CheckerboardMaterial(1, 0.8, 1.0,
                                         Color(0.9,0.9,0.9), Color(0.1,0.1,0.1))

        # Espelho 1: plano y = -4  (normal aponta em +y)
        self.add(Plane(Vector3D(0, -4, 0), Vector3D(0,  1, 0)), mirror)
        # Espelho 2: plano y = +4  (normal aponta em -y)
        self.add(Plane(Vector3D(0,  4, 0), Vector3D(0, -1, 0)), mirror2)

        # Objeto interessante no meio (esfera laranja)
        self.add(Ball(Vector3D(3, 0, 1.5), 0.6), mat_ball)
        self.add(Ball(Vector3D(6, 0, 1.5), 0.4), mat_ball)

        # Teto e chao para dar profundidade
        self.add(PlaneUV(Vector3D(0,0, 0), Vector3D(0,0, 1), Vector3D(1,0,0)), mat_floor)
        self.add(Plane  (Vector3D(0,0, 4), Vector3D(0,0,-1)),
                 SimpleMaterialWithShadows(0.05,0.5,Color(0.3,0.3,0.5),0.1,Color(1,1,1),32))
