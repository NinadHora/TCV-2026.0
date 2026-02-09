from src.shapes import ImplicitFunction
from src.base import BaseScene, Color

# class name should be Scene
class Scene(BaseScene):
    def __init__(self):
        super().__init__("Ellipse Scene")
        self.background = Color(1, 1, 1)

        # Define an ellipse using an implicit function
        def ellipse_func(point):
            x, y = point
            h, k = 4, 3  # center of the ellipse
            a, b = 3, 2  # semi-major and semi-minor axes
            return ((x - h) ** 2) / (a ** 2) + ((y - k) ** 2) / (b ** 2) - 1

        self.add(ImplicitFunction(ellipse_func), Color(0, 0, 1))  # Blue ellipse