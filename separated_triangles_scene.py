from src.base import BaseScene, Color
from src.shapes import Triangle

class Scene(BaseScene):
    def __init__(self, gap=1.0):
        super().__init__("Separated Triangles Scene")
        self.background = Color(1, 1, 1)

        # Triângulo esquerdo
        self.add(Triangle((1.0, 1.0), (3.0, 1.0), (2.0, 3.0)), Color(1.0, 0.0, 0.0))
        # Triângulo direito, afastado por 'gap'
        offset = 3.0 + gap
        self.add(Triangle((offset, 1.0), (offset + 2.0, 1.0), (offset + 1.0, 3.0)), Color(0.0, 0.0, 1.0))