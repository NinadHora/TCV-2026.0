"""
Tarefa 3 – Superficies implicitas: Mitchell e Coracao
Cena criativa: as duas superficies lado a lado num chao escuro
"""
import math
import numpy as np
from src.base import BaseScene, Color
from src.shapes import PlaneUV, ObjectTransform, mitchell_surface, heart_surface
from src.camera import Camera
from src.vector3d import Vector3D
from src.light import AreaLight
from src.materials import SimpleMaterialWithShadows, CheckerboardMaterial


class Scene(BaseScene):
    def __init__(self):
        super().__init__("Task 3 – Implicit Surfaces")
        self.background    = Color(0.05, 0.05, 0.1)
        self.ambient_light = Color(0.1, 0.1, 0.12)
        self.max_depth     = 4

        self.camera = Camera(
            eye     = Vector3D(0, -10, 4),
            look_at = Vector3D(0,   0, 0),
            up      = Vector3D(0,   0, 1),
            fov=35, img_width=800, img_height=600
        )
        self.lights = [
            AreaLight(
                position=Vector3D(-5, -5, 10),
                look_at=Vector3D(0, 0, 0),
                up=Vector3D(0, 0, 1),
                width=5, height=5,
                color=Color(1, 0.9, 0.8), intensity=2.2
            ),
            AreaLight(
                position=Vector3D(6, -2, 5),
                look_at=Vector3D(0, 0, 0),
                up=Vector3D(0, 0, 1),
                width=3, height=3,
                color=Color(0.4, 0.6, 1.0), intensity=1.0
            )
        ]

        mat_mitchell = SimpleMaterialWithShadows(0.05, 0.5, Color(0.2, 0.5, 0.9),
                                                 0.7, Color(1,1,1), 128)
        mat_heart    = SimpleMaterialWithShadows(0.05, 0.5, Color(0.9, 0.1, 0.15),
                                                 0.8, Color(1, 0.8, 0.8), 200)
        checker      = CheckerboardMaterial(1, 0.7, 1.5,
                                            Color(0.85,0.85,0.85), Color(0.08,0.08,0.08))

        # Mitchell a esquerda, escalado para ficar mais visivel
        M_m = [[0.7,0,0],[0,0.7,0],[0,0,0.7]]
        self.add(
            ObjectTransform(mitchell_surface(n_steps=80), M_m,
                            translation=Vector3D(-3.0, 0, 1.2)),
            mat_mitchell
        )

        # Coracao a direita (a orientacao original deixa o coracao "deitado";
        # rotacionar 90 graus em torno de X para ficar de pe)
        angle = math.radians(-90)
        Rx = [[1, 0,            0           ],
              [0, math.cos(angle), -math.sin(angle)],
              [0, math.sin(angle),  math.cos(angle)]]
        M_h = np.array(Rx) @ np.array([[1.2,0,0],[0,1.2,0],[0,0,1.2]])
        self.add(
            ObjectTransform(heart_surface(n_steps=80), M_h.tolist(),
                            translation=Vector3D(3.0, 0, 1.5)),
            mat_heart
        )

        # Chao
        self.add(PlaneUV(Vector3D(0,0,-0.5), Vector3D(0,0,1), Vector3D(1,0,0)), checker)
