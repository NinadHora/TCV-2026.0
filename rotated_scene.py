import os
import math
from src.shapes import ImplicitFunction, Triangle
from src.base import BaseScene, Color

class Scene(BaseScene):
    def __init__(self):
        super().__init__("Rotated Implicit Scene")
        self.background = Color(1, 1, 1)

        angle_deg = float(os.environ.get("ANGLE", "45"))
        theta = math.radians(angle_deg)
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)

        # Rotaciona invertendo: para saber se ponto (x,y) está dentro
        # da forma rotacionada, testamos o ponto rotacionado inversamente
        def f(point):
            x, y = point
            # Rotação inversa em torno da origem
            rx = cos_t * x + sin_t * y
            ry = -sin_t * x + cos_t * y
            return (0.004
                    + 0.110 * rx
                    - 0.177 * ry
                    - 0.174 * rx**2
                    + 0.224 * rx * ry
                    - 0.303 * ry**2
                    - 0.168 * rx**3
                    + 0.327 * rx**2 * ry
                    - 0.087 * rx * ry**2
                    - 0.013 * ry**3
                    + 0.235 * rx**4
                    - 0.667 * rx**3 * ry
                    + 0.745 * rx**2 * ry**2
                    - 0.029 * rx * ry**3
                    + 0.072 * ry**4)

        self.add(ImplicitFunction(f), Color(0.2, 0.5, 0.8))