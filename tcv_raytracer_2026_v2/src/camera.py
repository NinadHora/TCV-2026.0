"""
camera.py  –  Camera original + ThinLensCamera (Tarefa 5: profundidade de campo)
"""
import math
import random

from .ray import Ray
from .vector3d import Vector3D


class Camera:
    """Camera pinhole original."""

    def __init__(self, eye, look_at, up, fov, img_width, img_height):
        self.eye       = eye
        self.img_width  = img_width
        self.img_height = img_height

        aspect_ratio = img_height / img_width
        self.su = 2 * math.tan(math.radians(fov) / 2)
        self.sv = self.su * aspect_ratio

        self.w = (eye - look_at).normalize()
        self.u = up.normalize().cross(self.w).normalize()
        self.v = self.w.cross(self.u).normalize()

    def point_image2world(self, x, y):
        x_ndc = self.su * x / self.img_width  - self.su / 2
        y_ndc = self.sv * y / self.img_height - self.sv / 2
        return self.eye + self.u * x_ndc + self.v * y_ndc - self.w

    def ray(self, x, y):
        p = self.point_image2world(x, y)
        return Ray(self.eye, (p - self.eye).normalize())


# ---------------------------------------------------------------------------
# Tarefa 5 – ThinLensCamera (profundidade de campo)
#
# Ideia:
#   A camera pinhole gera um unico raio por pixel. A camera de lente fina
#   amostra um disco de raio `lens_radius` no plano da lente e direciona
#   todos os raios para o mesmo ponto no plano focal (distancia `focal_dist`).
#   Pixels fora do plano focal aparecem borrados porque os raios chegam de
#   posicoes ligeiramente diferentes na lente, mas convergem so no plano focal.
# ---------------------------------------------------------------------------

class ThinLensCamera(Camera):
    """
    Camera de lente fina para profundidade de campo.

    Parametros extras em relacao a Camera:
        lens_radius  – raio da abertura da lente (0 = pinhole)
        focal_dist   – distancia do plano focal em relacao ao olho
    """

    def __init__(self, eye, look_at, up, fov, img_width, img_height,
                 lens_radius=0.1, focal_dist=None):
        super().__init__(eye, look_at, up, fov, img_width, img_height)
        self.lens_radius = lens_radius
        # Se focal_dist nao especificado, usar a distancia ate look_at
        if focal_dist is None:
            focal_dist = (eye - look_at).length()
        self.focal_dist = focal_dist

    def _sample_disk(self):
        """Amostra uniforme num disco unitario (rejeicao)."""
        while True:
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            if x*x + y*y <= 1.0:
                return x, y

    def ray(self, x, y):
        # 1. Ponto no plano da imagem (como na camera pinhole)
        p_img = self.point_image2world(x, y)
        primary_dir = (p_img - self.eye).normalize()

        # 2. Ponto focal: onde o raio primario cruza o plano focal
        #    t_focal = focal_dist / cos(angulo entre direcao e -w)
        #    Equivalente: ponto = eye + primary_dir * (focal_dist / (-primary_dir.dot(w)))
        cos_angle = -primary_dir.dot(self.w)
        if abs(cos_angle) < 1e-6:
            return Ray(self.eye, primary_dir)
        t_focal = self.focal_dist / cos_angle
        focal_point = self.eye + primary_dir * t_focal

        # 3. Amostrar posicao na lente (disco no plano uv da camera)
        dx, dy = self._sample_disk()
        lens_pos = (self.eye
                    + self.u * (dx * self.lens_radius)
                    + self.v * (dy * self.lens_radius))

        # 4. Raio: da posicao na lente ate o ponto focal
        direction = (focal_point - lens_pos).normalize()
        return Ray(lens_pos, direction)
