"""
Tarefa 1 – Cubo e Cilindro
Cena: chao xadrez + cubo vermelho + cilindro azul
"""
import math
from src.base import BaseScene, Color
from src.shapes import Ball, Cube, Cylinder, PlaneUV
from src.camera import Camera
from src.vector3d import Vector3D
from src.light import AreaLight
from src.materials import SimpleMaterialWithShadows, CheckerboardMaterial

class Scene(BaseScene):
    def __init__(self):
        super().__init__("Task 1 – Cube & Cylinder")
        self.background   = Color(0.55, 0.75, 1.0)
        self.ambient_light = Color(0.15, 0.15, 0.15)
        self.max_depth    = 4

        self.camera = Camera(
            eye     = Vector3D(6, -8, 5),
            look_at = Vector3D(0,  0, 1),
            up      = Vector3D(0,  0, 1),
            fov=35, img_width=800, img_height=600
        )
        self.lights = [AreaLight(
            position=Vector3D(5, -3, 10),
            look_at=Vector3D(0, 0, 0),
            up=Vector3D(0, 0, 1),
            width=4, height=4,
            color=Color(1,1,1), intensity=1.8
        )]

        red = SimpleMaterialWithShadows(0.05, 0.7, Color(0.8,0.1,0.1),
                                        0.4, Color(1,1,1), 64)
        blue = SimpleMaterialWithShadows(0.05, 0.7, Color(0.1,0.2,0.9),
                                         0.4, Color(1,1,1), 64)
        gold = SimpleMaterialWithShadows(0.05, 0.6, Color(0.9,0.7,0.1),
                                         0.5, Color(1,1,0.8), 128)

        # Cubo vermelho centrado em (0,0,1), semi-extensao 1
        self.add(Cube(half_size=1.0), red)
        # Cilindro azul ao lado
        self.add(Cylinder(radius=0.6, half_height=1.4), blue)
        # Esfera dourada em cima do cubo, so para referencia
        self.add(Ball(center=Vector3D(0, 0, 2.6), radius=0.55), gold)

        # Plano xadrez no chao
        checker = CheckerboardMaterial(1, 0.8, 1.0,
                                       Color(0.95,0.95,0.95), Color(0.15,0.15,0.15))
        self.add(PlaneUV(Vector3D(0,0,-1), Vector3D(0,0,1), Vector3D(1,0,0)), checker)

        # Mover cilindro para (3, 0, z) via translacao direta na cena
        # (ObjectTransform sera usado na Tarefa 2)
        # — re-adicionar cilindro deslocado manualmente
        # Para isso precisamos de ObjectTransform; aqui apenas demonstramos as formas puras.
        # O cilindro acima ja esta centrado na origem.  Vamos adicionar outro deslocado
        # usando a logica mais simples possivel: criar outro objeto em posicao diferente.
        # (Cubo e Cilindro sao sempre centrados na origem => usamos ObjectTransform na T2.)
