from src.shapes import ImplicitFunction
from src.base import BaseScene, Color

class Scene(BaseScene):
    def __init__(self):
        super().__init__("Mandelbrot Scene")
        self.background = Color(0, 0, 0)

        def mandelbrot(point):
            cx, cy = point
            zx, zy = 0.0, 0.0
            max_iter = 100
            for _ in range(max_iter):
                if zx * zx + zy * zy > 4.0:
                    return 1  # fora (positivo = não pertence)
                zx, zy = zx * zx - zy * zy + cx, 2 * zx * zy + cy
            return -1  # dentro (negativo = pertence)

        self.add(ImplicitFunction(mandelbrot), Color(1.0, 1.0, 1.0))