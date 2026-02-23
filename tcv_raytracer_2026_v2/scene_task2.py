"""
Tarefa 2 – ObjectTransform
Cena: paraboloide (esfera escalada), cubo rotacionado, cilindro esticado
"""
import math
import numpy as np
from src.base import BaseScene, Color
from src.shapes import Ball, Cube, Cylinder, PlaneUV, ObjectTransform
from src.camera import Camera
from src.vector3d import Vector3D
from src.light import AreaLight, PointLight
from src.materials import SimpleMaterialWithShadows, CheckerboardMaterial


def Ry(deg):
    """Matriz de rotacao em torno de Y."""
    t = math.radians(deg)
    return [[math.cos(t), 0, math.sin(t)],
            [0,           1, 0          ],
            [-math.sin(t),0, math.cos(t)]]

def Rz(deg):
    t = math.radians(deg)
    return [[math.cos(t), -math.sin(t), 0],
            [math.sin(t),  math.cos(t), 0],
            [0,            0,           1]]

def scale(sx, sy, sz):
    return [[sx,0,0],[0,sy,0],[0,0,sz]]


class Scene(BaseScene):
    def __init__(self):
        super().__init__("Task 2 – ObjectTransform")
        self.background    = Color(0.2, 0.2, 0.35)
        self.ambient_light = Color(0.12, 0.12, 0.12)
        self.max_depth     = 4

        self.camera = Camera(
            eye     = Vector3D(8, -10, 6),
            look_at = Vector3D(0,   0, 1),
            up      = Vector3D(0,   0, 1),
            fov=38, img_width=800, img_height=600
        )
        self.lights = [AreaLight(
            position=Vector3D(4, -4, 12),
            look_at=Vector3D(0, 0, 0),
            up=Vector3D(0, 0, 1),
            width=6, height=6,
            color=Color(1,1,1), intensity=2.0
        )]

        mat_red    = SimpleMaterialWithShadows(0.05, 0.7, Color(0.9,0.15,0.15), 0.5, Color(1,1,1), 80)
        mat_green  = SimpleMaterialWithShadows(0.05, 0.7, Color(0.1,0.75,0.2 ), 0.4, Color(1,1,1), 64)
        mat_purple = SimpleMaterialWithShadows(0.05, 0.6, Color(0.6,0.1,0.9  ), 0.6, Color(1,1,1), 128)
        mat_teal   = SimpleMaterialWithShadows(0.05, 0.7, Color(0.1,0.8,0.75 ), 0.4, Color(1,1,1), 64)
        checker    = CheckerboardMaterial(1, 0.8, 1.0,
                                          Color(0.95,0.95,0.95), Color(0.1,0.1,0.1))

        # 1. Paraboloide: esfera unitaria escalada (rx=1.5, ry=0.6, rz=1.5)
        #    colocada em (-3, 1, 0) via translacao
        self.add(
            ObjectTransform(Ball(Vector3D(0,0,0), 1.0),
                            scale(1.5, 0.6, 1.5),
                            translation=Vector3D(-3, 1, 0.6)),
            mat_red
        )

        # 2. Cubo rotacionado 35 graus em torno de Z, depois escalonado
        M_cube = np.array(Rz(35)) @ np.array(scale(1.0, 1.0, 1.4))
        self.add(
            ObjectTransform(Cube(1.0), M_cube.tolist(),
                            translation=Vector3D(0, 0, 1.0)),
            mat_green
        )

        # 3. Cilindro inclinado 45 graus em torno de Y, esticado
        M_cyl = np.array(Ry(45)) @ np.array(scale(0.5, 0.5, 2.0))
        self.add(
            ObjectTransform(Cylinder(1.0, 1.0), M_cyl.tolist(),
                            translation=Vector3D(3.2, 0.5, 1.5)),
            mat_purple
        )

        # 4. Esfera simples (sem transformacao) para referencia
        self.add(Ball(Vector3D(-3, -2.5, 0.7), 0.7), mat_teal)

        # Chao
        self.add(PlaneUV(Vector3D(0,0,-1), Vector3D(0,0,1), Vector3D(1,0,0)), checker)
