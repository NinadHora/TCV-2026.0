from src.base import BaseScene, Color
from src.shapes import Circle

# class name should be Scene
class Scene(BaseScene):
    def __init__(self):
        super().__init__("Mickey Scene")
        self.background = Color(1, 1, 1)

        # Foreground first so it paints over shapes behind it.
        # Mouth + tongue (smaller)
        self.add(Circle((4.0, 1.45), 0.48), Color(0.05, 0.05, 0.05))  # Mouth
        self.add(Circle((4.0, 1.35), 0.28), Color(0.85, 0.15, 0.15))  # Tongue
        # Pupils
        self.add(Circle((3.62, 2.55), 0.14), Color(0.05, 0.05, 0.05))  # Left pupil
        self.add(Circle((4.38, 2.55), 0.14), Color(0.05, 0.05, 0.05))  # Right pupil
        # Eyes (larger)
        self.add(Circle((3.62, 2.7), 0.48), Color(1.0, 1.0, 1.0))  # Left eye
        self.add(Circle((4.38, 2.7), 0.48), Color(1.0, 1.0, 1.0))  # Right eye
        # Muzzle + face
        self.add(Circle((4.0, 1.9), 0.95), Color(1.0, 0.88, 0.72))  # Muzzle
        self.add(Circle((4.0, 2.2), 1.45), Color(1.0, 0.85, 0.65))  # Face
        # Head + ears behind
        self.add(Circle((4.0, 2.7), 2.05), Color(0.05, 0.05, 0.05))  # Head
        self.add(Circle((2.3, 4.6), 1.05), Color(0.05, 0.05, 0.05))  # Left ear
        self.add(Circle((5.7, 4.6), 1.05), Color(0.05, 0.05, 0.05))  # Right ear
