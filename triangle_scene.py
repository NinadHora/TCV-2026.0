from src.base import BaseScene, Color
from src.shapes import Triangle

# class name should be Scene
class Scene(BaseScene):
    def __init__(self):
        super().__init__("Triangle Scene")
        self.background = Color(1, 1, 1)

        # Add some triangles to the scene
        self.add(Triangle((1.0, 1.0), (3.0, 1.0), (2.0, 3.0)), Color(1.0, 0.0, 0.0))  # Red triangle
