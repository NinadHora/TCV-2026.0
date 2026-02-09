from src.shapes import Triangle
from src.base import BaseScene, Color

# class name should be "Scene"
class Scene(BaseScene):
    def __init__(self):
        super().__init__("Lion Scene")
        self.background = Color(1, 1, 1)
        self.file = "lion.txt"

        max_x, max_y = -10000.0, -10000.0
        min_x, min_y = 10000.0, 10000.0

        with open(self.file, 'r') as f:
            lines = f.readlines()

        for line in lines[::-1]:
            r, g, b, x1, y1, x2, y2, x3, y3 = list(map(float, line.strip().split()))
            # lion is upside down in the file
            y1 = -y1 + 381
            y2 = -y2 + 381
            y3 = -y3 + 381

            v1 = (x1, y1)
            v2 = (x2, y2)
            v3 = (x3, y3)
            max_x = max(max_x, x1, x2, x3)
            max_y = max(max_y, y1, y2, y3)
            min_x = min(min_x, x1, x2, x3)
            min_y = min(min_y, y1, y2, y3)
            self.add(Triangle(v1, v2, v3), Color(r, g, b))  # Colored triangles
        
        print(f"Lion bounding box: x({min_x}, {max_x}), y({min_y}, {max_y})")