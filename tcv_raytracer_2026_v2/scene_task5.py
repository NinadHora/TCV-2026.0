"""
Tarefa 5 – Profundidade de Campo (Depth of Field)
Usa ThinLensCamera. Varie lens_radius para mudar o bokeh.
Cena: fileira de esferas coloridas a distancias diferentes.
O plano focal aponta para a esfera do meio.
"""
import math
from src.base import BaseScene, Color
from src.shapes import Ball, PlaneUV
from src.camera import ThinLensCamera
from src.vector3d import Vector3D
from src.light import AreaLight
from src.materials import SimpleMaterialWithShadows, CheckerboardMaterial


class Scene(BaseScene):
    def __init__(self):
        super().__init__("Task 5 – Depth of Field")
        self.background    = Color(0.6, 0.75, 1.0)
        self.ambient_light = Color(0.12, 0.12, 0.12)
        self.max_depth     = 4

        eye     = Vector3D(-10, 0, 2.5)
        look_at = Vector3D(  0, 0, 2.5)   # foco na esfera central

        self.camera = ThinLensCamera(
            eye        = eye,
            look_at    = look_at,
            up         = Vector3D(0, 0, 1),
            fov        = 35,
            img_width  = 800,
            img_height = 600,
            lens_radius = 0.35,   # <-- varie: 0.0 = pinhole, 0.8 = muito desfocado
            focal_dist  = (eye - look_at).length()   # ~10 unidades
        )

        self.lights = [AreaLight(
            position=Vector3D(-5, -8, 12),
            look_at=Vector3D(0, 0, 2),
            up=Vector3D(0, 0, 1),
            width=6, height=6,
            color=Color(1,1,1), intensity=2.0
        )]

        colors = [
            Color(0.9, 0.15, 0.15),   # vermelho   z= -6
            Color(0.9, 0.55, 0.1 ),   # laranja    z= -3
            Color(0.15, 0.7, 0.2 ),   # verde      z=  0  <- FOCO
            Color(0.15, 0.4, 0.9 ),   # azul       z= +3
            Color(0.7,  0.1, 0.85),   # roxo       z= +6
        ]
        y_positions = [-6, -3, 0, 3, 6]

        for y, c in zip(y_positions, colors):
            mat = SimpleMaterialWithShadows(0.05, 0.7, c, 0.5, Color(1,1,1), 100)
            self.add(Ball(Vector3D(0, y, 2.5), 0.9), mat)

        checker = CheckerboardMaterial(1, 0.8, 1.5,
                                       Color(0.95,0.95,0.95), Color(0.1,0.1,0.1))
        self.add(PlaneUV(Vector3D(0,0,0), Vector3D(0,0,1), Vector3D(1,0,0)), checker)
