from src.base import BaseScene, Color
from src.shapes import Triangle

class Scene(BaseScene):
    def __init__(self):
        super().__init__("Two Adjacent Triangles Scene")
        self.background = Color(1, 1, 1)

        # Dois triângulos formando um quadrado, compartilhando a diagonal
        self.add(Triangle((2.0, 1.0), (5.0, 1.0), (5.0, 4.0)), Color(1.0, 0.0, 0.0))  # Vermelho
        self.add(Triangle((2.0, 1.0), (5.0, 4.0), (2.0, 4.0)), Color(0.0, 0.0, 1.0))  # Azul