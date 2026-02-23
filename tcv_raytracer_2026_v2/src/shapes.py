"""
shapes.py  –  todas as primitivas do raytracer
Tarefas implementadas:
  1. Cube, Cylinder
  2. ObjectTransform  (transformação 3x3 + translação)
  3. ImplicitSurface, mitchell_surface(), heart_surface()
"""

import math
import numpy as np

from .vector3d import Vector3D
from .base import Shape, HitRecord, CastEpsilon


# ---------------------------------------------------------------------------
# Formas originais
# ---------------------------------------------------------------------------

class Ball(Shape):
    def __init__(self, center, radius):
        super().__init__("ball")
        self.center = center
        self.radius = radius

    def hit(self, ray):
        oc = ray.origin - self.center
        a = ray.direction.dot(ray.direction)
        b = 2.0 * oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius * self.radius
        disc = b*b - 4*a*c
        if disc < 0:
            return HitRecord(False, float('inf'), None, None)
        t = (-b - disc**0.5) / (2*a)
        if t > CastEpsilon:
            p = ray.point_at_parameter(t)
            return HitRecord(True, t, p, (p - self.center).normalize())
        t = (-b + disc**0.5) / (2*a)
        if t > CastEpsilon:
            p = ray.point_at_parameter(t)
            return HitRecord(True, t, p, (p - self.center).normalize())
        return HitRecord(False, float('inf'), None, None)


class Plane(Shape):
    def __init__(self, point, normal):
        super().__init__("plane")
        self.point = point
        self.normal = normal.normalize()

    def hit(self, ray):
        denom = self.normal.dot(ray.direction)
        if abs(denom) > 1e-6:
            t = (self.point - ray.origin).dot(self.normal) / denom
            if t >= CastEpsilon:
                return HitRecord(True, t, ray.point_at_parameter(t), self.normal)
        return HitRecord(False, float('inf'), None, None)


class PlaneUV(Shape):
    def __init__(self, point, normal, forward_direction):
        super().__init__("plane")
        self.point = point
        self.normal = normal.normalize()
        self.forward_direction = forward_direction.normalize()
        self.right_direction = self.normal.cross(self.forward_direction).normalize()

    def hit(self, ray):
        denom = self.normal.dot(ray.direction)
        if abs(denom) > 1e-6:
            t = (self.point - ray.origin).dot(self.normal) / denom
            if t >= CastEpsilon:
                point = ray.point_at_parameter(t)
                vec = point - self.point
                uv = Vector3D(vec.dot(self.right_direction), vec.dot(self.forward_direction), 0)
                return HitRecord(True, t, point, self.normal, uv=uv)
        return HitRecord(False, float('inf'), None, None)


# ---------------------------------------------------------------------------
# Tarefa 1.1 – Cube
# Cubo centrado na origem, semi-extensao = half_size em cada eixo
# ---------------------------------------------------------------------------

class Cube(Shape):
    """Cubo centrado na origem, semi-extensao `half_size`."""

    def __init__(self, half_size=1.0):
        super().__init__("cube")
        self.hs = half_size

    def hit(self, ray):
        ox, oy, oz = ray.origin.x, ray.origin.y, ray.origin.z
        dx, dy, dz = ray.direction.x, ray.direction.y, ray.direction.z
        hs = self.hs

        tmin = float('-inf')
        tmax = float('inf')
        normal_tmin = Vector3D(0, 0, 1)

        for (o, d, axis) in [(ox, dx, 0), (oy, dy, 1), (oz, dz, 2)]:
            if abs(d) < 1e-8:
                if o < -hs or o > hs:
                    return HitRecord(False, float('inf'), None, None)
            else:
                t1 = (-hs - o) / d
                t2 = ( hs - o) / d
                # normal da face mais proxima (entrada)
                n1 = [0.0, 0.0, 0.0]
                n1[axis] = -1.0 if d > 0 else 1.0
                if t1 > t2:
                    t1, t2 = t2, t1
                    n1[axis] *= -1
                if t1 > tmin:
                    tmin = t1
                    normal_tmin = Vector3D(*n1)
                tmax = min(tmax, t2)
                if tmin > tmax:
                    return HitRecord(False, float('inf'), None, None)

        if tmin > CastEpsilon:
            t, normal = tmin, normal_tmin
        elif tmax > CastEpsilon:
            t = tmax
            p = ray.point_at_parameter(t)
            normal = self._face_normal(p.x, p.y, p.z)
        else:
            return HitRecord(False, float('inf'), None, None)

        point = ray.point_at_parameter(t)
        return HitRecord(True, t, point, normal)

    def _face_normal(self, px, py, pz):
        hs, eps = self.hs, 1e-3 * self.hs
        if abs(abs(px) - hs) < eps: return Vector3D(1 if px > 0 else -1, 0, 0)
        if abs(abs(py) - hs) < eps: return Vector3D(0, 1 if py > 0 else -1, 0)
        return Vector3D(0, 0, 1 if pz > 0 else -1)


# ---------------------------------------------------------------------------
# Tarefa 1.2 – Cylinder
# Cilindro eixo Z, raio `radius`, semi-altura `half_height`, centrado na origem
# ---------------------------------------------------------------------------

class Cylinder(Shape):
    """Cilindro fechado, eixo Z, raio `radius`, altura 2*`half_height`."""

    def __init__(self, radius=1.0, half_height=1.0):
        super().__init__("cylinder")
        self.radius = radius
        self.hh = half_height

    def hit(self, ray):
        ox, oy, oz = ray.origin.x, ray.origin.y, ray.origin.z
        dx, dy, dz = ray.direction.x, ray.direction.y, ray.direction.z
        r, hh = self.radius, self.hh
        candidates = []

        # Corpo lateral
        a = dx*dx + dy*dy
        if abs(a) > 1e-8:
            b = 2*(ox*dx + oy*dy)
            c = ox*ox + oy*oy - r*r
            disc = b*b - 4*a*c
            if disc >= 0:
                sq = math.sqrt(max(disc, 0))
                for sign in (-1, 1):
                    t = (-b + sign*sq) / (2*a)
                    if t > CastEpsilon:
                        pz = oz + t*dz
                        if -hh <= pz <= hh:
                            px = ox + t*dx
                            py = oy + t*dy
                            candidates.append((t, Vector3D(px/r, py/r, 0)))

        # Tampas
        if abs(dz) > 1e-8:
            for cap_z, cap_n in [(-hh, Vector3D(0,0,-1)), (hh, Vector3D(0,0,1))]:
                t = (cap_z - oz) / dz
                if t > CastEpsilon:
                    px = ox + t*dx; py = oy + t*dy
                    if px*px + py*py <= r*r:
                        candidates.append((t, cap_n))

        if not candidates:
            return HitRecord(False, float('inf'), None, None)
        t, normal = min(candidates, key=lambda h: h[0])
        return HitRecord(True, t, ray.point_at_parameter(t), normal)


# ---------------------------------------------------------------------------
# Helpers numpy <-> Vector3D
# ---------------------------------------------------------------------------

def _v2a(v):
    return np.array([v.x, v.y, v.z], dtype=float)

def _a2v(a):
    return Vector3D(float(a[0]), float(a[1]), float(a[2]))


# ---------------------------------------------------------------------------
# Tarefa 2 – ObjectTransform
#
# Por que M^{-T} para normais?
# A normal n satisfaz n.t = 0 para todo tangente t na superficie.
# Apos a transformacao M, tangentes viram Mt.
# Queremos n' tal que n'.(Mt) = 0, i.e. (An)^T (Mt) = n^T A^T M t = 0.
# Logo A^T M = I => A = (M^{-1})^T = M^{-T}.
# ---------------------------------------------------------------------------

class ObjectTransform(Shape):
    """
    Envolve qualquer Shape com transformacao afim:  p_world = M * p_obj + T

    Parametros
    ----------
    shape       : Shape
    matrix      : array-like 3x3 (parte linear)
    translation : Vector3D  (deslocamento; default = origem)
    """

    def __init__(self, shape, matrix, translation=None):
        super().__init__("object_transform")
        self.shape = shape
        self.M     = np.array(matrix, dtype=float)
        self.M_inv = np.linalg.inv(self.M)
        self.M_inv_T = self.M_inv.T
        self.T = _v2a(translation) if translation else np.zeros(3)

    def _to_obj_pt(self, world_pt):
        return self.M_inv @ (_v2a(world_pt) - self.T)

    def _to_world_pt(self, obj_pt):
        return _a2v(self.M @ _v2a(obj_pt) + self.T)

    def _to_world_n(self, obj_n):
        arr = self.M_inv_T @ _v2a(obj_n)
        mag = float(np.linalg.norm(arr))
        return _a2v(arr / mag) if mag > 1e-10 else obj_n

    def hit(self, ray):
        from .ray import Ray
        # Levar raio ao espaco do objeto
        o_obj = _a2v(self._to_obj_pt(ray.origin))
        d_arr = self.M_inv @ _v2a(ray.direction)
        d_len = float(np.linalg.norm(d_arr))
        if d_len < 1e-10:
            return HitRecord(False, float('inf'), None, None)
        d_obj = _a2v(d_arr / d_len)

        rec = self.shape.hit(Ray(o_obj, d_obj, ray.depth))
        if not rec.hit:
            return rec

        # t_world = t_obj / d_len  (escala de comprimento muda com M)
        t_world = rec.t / d_len
        return HitRecord(True, t_world,
                         self._to_world_pt(rec.point),
                         self._to_world_n(rec.normal),
                         material=rec.material, ray=ray, uv=rec.uv)


# ---------------------------------------------------------------------------
# Tarefa 3 – Superficies implicitas  f(x,y,z) = 0
# Algoritmo: AABB -> amostras uniformes -> bissecao em mudancas de sinal
# ---------------------------------------------------------------------------

def _gradient(f, x, y, z, eps=1e-4):
    gx = (f(x+eps, y, z) - f(x-eps, y, z)) / (2*eps)
    gy = (f(x, y+eps, z) - f(x, y-eps, z)) / (2*eps)
    gz = (f(x, y, z+eps) - f(x, y, z-eps)) / (2*eps)
    return Vector3D(gx, gy, gz)


class ImplicitSurface(Shape):
    """
    Superficie implicita f(x,y,z)=0 confinada a uma AABB.

    1. Teste raio-AABB  (pulo rapido se nao acerta)
    2. Amostragem uniforme no segmento interior
    3. Bissecao em intervalos com mudanca de sinal
    4. Normal = gradiente numerico de f
    """

    def __init__(self, func, bbox_min, bbox_max, n_steps=80):
        super().__init__("implicit_surface")
        self.func    = func
        self.bmin    = bbox_min
        self.bmax    = bbox_max
        self.n_steps = n_steps

    def _aabb_hit(self, ray):
        tmin, tmax = float('-inf'), float('inf')
        bmin = [self.bmin.x, self.bmin.y, self.bmin.z]
        bmax = [self.bmax.x, self.bmax.y, self.bmax.z]
        o = [ray.origin.x,    ray.origin.y,    ray.origin.z]
        d = [ray.direction.x, ray.direction.y, ray.direction.z]
        for i in range(3):
            if abs(d[i]) < 1e-8:
                if o[i] < bmin[i] or o[i] > bmax[i]: return None
            else:
                t1 = (bmin[i]-o[i])/d[i]; t2 = (bmax[i]-o[i])/d[i]
                if t1 > t2: t1, t2 = t2, t1
                tmin = max(tmin, t1); tmax = min(tmax, t2)
                if tmin > tmax: return None
        if tmax < CastEpsilon: return None
        return (max(tmin, CastEpsilon), tmax)

    def _f(self, ray, t):
        p = ray.point_at_parameter(t)
        return self.func(p.x, p.y, p.z)

    def hit(self, ray):
        interval = self._aabb_hit(ray)
        if interval is None:
            return HitRecord(False, float('inf'), None, None)

        t0, t1 = interval
        step = (t1 - t0) / self.n_steps
        ts = [t0 + i*step for i in range(self.n_steps + 1)]
        fs = [self._f(ray, t) for t in ts]

        best_t = None
        for i in range(len(ts) - 1):
            if fs[i] * fs[i+1] <= 0:
                a, b = ts[i], ts[i+1]; fa = fs[i]
                for _ in range(48):
                    mid = 0.5*(a+b); fm = self._f(ray, mid)
                    if fa*fm <= 0: b = mid
                    else: a, fa = mid, fm
                rt = 0.5*(a+b)
                if rt > CastEpsilon and (best_t is None or rt < best_t):
                    best_t = rt

        if best_t is None:
            return HitRecord(False, float('inf'), None, None)

        p = ray.point_at_parameter(best_t)
        grad = _gradient(self.func, p.x, p.y, p.z)
        try:    normal = grad.normalize()
        except: normal = Vector3D(0, 1, 0)
        return HitRecord(True, best_t, p, normal)


# Funcoes no nivel do modulo para que o multiprocessing consiga serializá-las (pickle)
def _f_mitchell(x, y, z):
    r2 = y*y + z*z
    return 4*(x**4 + r2**2 + 17*x*x*r2) - 20*(x*x + r2) + 17

def _f_heart(x, y, z):
    a = x*x + (9.0/4)*y*y + z*z - 1.0
    return a**3 - x*x*z**3 - (9.0/80)*y*y*z**3


def mitchell_surface(n_steps=80):
    """f(x,y,z) = 4(x^4 + (y^2+z^2)^2 + 17x^2(y^2+z^2)) - 20(x^2+y^2+z^2) + 17"""
    return ImplicitSurface(_f_mitchell,
        Vector3D(-2.5,-2.5,-2.5), Vector3D(2.5,2.5,2.5), n_steps)


def heart_surface(n_steps=80):
    """f(x,y,z) = (x^2 + 9/4*y^2 + z^2 - 1)^3 - x^2*z^3 - 9/80*y^2*z^3"""
    return ImplicitSurface(_f_heart,
        Vector3D(-1.5,-1.5,-1.5), Vector3D(1.5,1.5,1.5), n_steps)


# Compatibilidade
class ImplicitFunction(Shape):
    def __init__(self, function):
        super().__init__("implicit_function")
        self.func = function
    def in_out(self, point):
        return self.func(point) <= 0
