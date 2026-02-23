"""
materials.py  – materiais originais + Tarefa 4: MirrorMaterial
"""
import math

from .base import Color, CastEpsilon, Material
from .ray import Ray
from .vector3d import Vector3D


class ColorMaterial(Material):
    def __init__(self, diffuse_color):
        super().__init__()
        self.diffuse_color = diffuse_color

    def shade(self, hit_record, scene):
        return self.diffuse_color


class SimpleMaterial(Material):
    def __init__(self, ambient_coefficient, diffuse_coefficient, diffuse_color,
                 specular_coefficient, specular_color, specular_shininess=32):
        super().__init__()
        self.ambient_coefficient  = ambient_coefficient
        self.diffuse_coefficient  = diffuse_coefficient
        self.diffuse_color        = diffuse_color
        self.specular_coefficient = specular_coefficient
        self.specular_color       = specular_color
        self.specular_shininess   = specular_shininess

    def shade(self, hit_record, scene):
        shaded = Color(0, 0, 0)
        amb = scene.ambient_light * self.ambient_coefficient
        for light in scene.lights:
            lv      = light.position() - hit_record.point
            ld      = lv.normalize()
            diff_i  = max(hit_record.normal.dot(ld), 0)
            diff    = (self.diffuse_color @ light.color) * (self.diffuse_coefficient * diff_i)
            vd      = (scene.camera.eye - hit_record.point).normalize()
            rd      = (hit_record.normal * 2 * hit_record.normal.dot(ld) - ld).normalize()
            spec_i  = max(vd.dot(rd), 0) ** self.specular_shininess
            spec    = (self.specular_color @ light.color) * self.specular_coefficient * spec_i
            shaded += (amb + diff + spec) * light.intensity
        return shaded


class SimpleMaterialWithShadows(SimpleMaterial):
    def shade(self, hit_record, scene):
        shaded = Color(0, 0, 0)
        amb    = scene.ambient_light * self.ambient_coefficient
        for light in scene.lights:
            shaded += amb * light.intensity
            lv  = light.position() - hit_record.point
            sr  = Ray(hit_record.point + hit_record.normal * CastEpsilon, lv.normalize())
            sh  = scene.hit(sr)
            if sh.hit and sh.t < lv.length():
                continue
            ld      = lv.normalize()
            diff_i  = max(hit_record.normal.dot(ld), 0)
            diff    = (self.diffuse_color @ light.color) * (self.diffuse_coefficient * diff_i)
            vd      = (scene.camera.eye - hit_record.point).normalize()
            rd      = (hit_record.normal * 2 * hit_record.normal.dot(ld) - ld).normalize()
            spec_i  = max(vd.dot(rd), 0) ** self.specular_shininess
            spec    = (self.specular_color @ light.color) * self.specular_coefficient * spec_i
            shaded += (diff + spec) * light.intensity
        return shaded


class CheckerboardMaterial(SimpleMaterial):
    def __init__(self, ambient_coefficient, diffuse_coefficient, square_size,
                 white_color=Color(1,1,1), black_color=Color(0,0,0)):
        super().__init__(ambient_coefficient, diffuse_coefficient, Color(0,0,0), 0, Color(0,0,0))
        self.square_size = square_size
        self.white_color = white_color
        self.black_color = black_color

    def shade(self, hit_record, scene):
        shaded = Color(0, 0, 0)
        amb    = scene.ambient_light * self.ambient_coefficient
        for light in scene.lights:
            shaded += amb * light.intensity
            lv  = light.position() - hit_record.point
            sr  = Ray(hit_record.point + hit_record.normal * CastEpsilon, lv.normalize())
            sh  = scene.hit(sr)
            if sh.hit and sh.t < lv.length():
                continue
            u = hit_record.uv.x / self.square_size
            v = hit_record.uv.y / self.square_size
            dc = self.white_color if (int(math.floor(u))+int(math.floor(v)))%2==0 else self.black_color
            ld      = lv.normalize()
            diff_i  = max(hit_record.normal.dot(ld), 0)
            diff    = (dc @ light.color) * (self.diffuse_coefficient * diff_i)
            shaded += diff * light.intensity
        return shaded


class TranslucidMaterial(SimpleMaterial):
    def __init__(self, ambient_coefficient, diffuse_coefficient, diffuse_color,
                 specular_coefficient, specular_color, specular_shininess=32,
                 transmission_coefficient=0.5, refraction_index=1.5):
        super().__init__(ambient_coefficient, diffuse_coefficient, diffuse_color,
                         specular_coefficient, specular_color, specular_shininess)
        self.transmission_coefficient = transmission_coefficient
        self.refraction_index = refraction_index

    def shade(self, hit_record, scene):
        shaded   = scene.ambient_light * self.ambient_coefficient
        origin   = hit_record.ray.origin
        view_dir = (origin - hit_record.point).normalize()
        eta = 1.0 / self.refraction_index
        c = hit_record.normal.dot(view_dir)
        n = hit_record.normal
        if c < 0:
            n   = -n; eta = 1.0/eta; c = -c

        for light in scene.lights:
            lv      = light.position() - hit_record.point
            ld      = lv.normalize()
            diff_i  = max(n.dot(ld), 0)
            shaded += (self.diffuse_color @ light.color) * (self.diffuse_coefficient * diff_i) * light.intensity
            rd      = (n * 2 * n.dot(ld) - ld).normalize()
            spec_i  = max(view_dir.dot(rd), 0) ** self.specular_shininess
            shaded += (self.specular_color @ light.color) * self.specular_coefficient * spec_i * light.intensity

        trans = Color(0, 0, 0)
        if hit_record.ray.depth < scene.max_depth:
            k = 1 - eta**2 * (1 - c**2)
            if k >= 0:
                rd = (-view_dir * eta + n * (eta*c - math.sqrt(k))).normalize()
                tr = Ray(hit_record.point, rd, hit_record.ray.depth + 1)
                th = scene.hit(tr)
                if th.hit:
                    trans = th.material.shade(th, scene) * self.transmission_coefficient
                else:
                    trans = scene.background * self.transmission_coefficient
            else:
                rd = (n * 2 * n.dot(view_dir) - view_dir).normalize()
                rr = Ray(hit_record.point, rd, hit_record.ray.depth + 1)
                rh = scene.hit(rr)
                if rh.hit:
                    trans = rh.material.shade(rh, scene) * self.transmission_coefficient
        else:
            trans = Color(0, 1, 0)

        return shaded + trans


# ---------------------------------------------------------------------------
# Tarefa 4 – MirrorMaterial
# Material puramente especular: reflete o raio sem componente difusa.
# ---------------------------------------------------------------------------

class MirrorMaterial(Material):
    """
    Espelho perfeito.  Reflexao pura, sem difusao.

    `reflectivity` (0-1): quanto da cor refletida contribui.
    `tint`               : cor multiplicativa do espelho (default branco).
    `ambient_coefficient`: pequena componente ambiente para o espelho nao
                           ficar completamente preto quando nao reflete nada.
    """

    def __init__(self, reflectivity=1.0, tint=None, ambient_coefficient=0.02):
        super().__init__()
        self.reflectivity        = reflectivity
        self.tint                = tint if tint else Color(1, 1, 1)
        self.ambient_coefficient = ambient_coefficient

    def shade(self, hit_record, scene):
        shaded = scene.ambient_light * self.ambient_coefficient

        if hit_record.ray.depth >= scene.max_depth:
            return shaded   # fim da recursao: espelho escuro

        # Calcula direcao de reflexao: r = d - 2(d.n)n  (d = direcao incidente)
        d = hit_record.ray.direction
        n = hit_record.normal
        # garante que a normal aponta contra o raio
        if d.dot(n) > 0:
            n = -n
        r = (d - n * (2 * d.dot(n))).normalize()

        reflect_ray = Ray(hit_record.point + n * CastEpsilon, r, hit_record.ray.depth + 1)
        reflect_hit = scene.hit(reflect_ray)

        if reflect_hit.hit:
            reflected_color = reflect_hit.material.shade(reflect_hit, scene)
        else:
            reflected_color = scene.background

        return shaded + (self.tint @ reflected_color) * self.reflectivity
