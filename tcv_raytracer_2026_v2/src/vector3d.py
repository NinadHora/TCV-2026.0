class Vector3D:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other: 'Vector3D') -> 'Vector3D':
        return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Vector3D') -> 'Vector3D':
        return self.__class__(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> 'Vector3D':
        return self.__class__(self.x * scalar, self.y * scalar, self.z * scalar)

    def __truediv__(self, scalar: float) -> 'Vector3D':
        return self.__class__(self.x / scalar, self.y / scalar, self.z / scalar)

    def dot(self, other: 'Vector3D') -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: 'Vector3D') -> 'Vector3D':
        return self.__class__(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def length(self) -> float:
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

    def normalize(self) -> 'Vector3D':
        mag = self.length()
        if mag == 0:
            raise ValueError("Cannot normalize a zero-length vector")
        return self.__class__(self.x / mag, self.y / mag, self.z / mag)

    def __matmul__(self, other: 'Vector3D') -> 'Vector3D':
        return self.__class__(self.x * other.x, self.y * other.y, self.z * other.z)

    def __str__(self) -> str:
        return f"Vector3D({self.x}, {self.y}, {self.z})"

    def __neg__(self) -> 'Vector3D':
        return self.__class__(-self.x, -self.y, -self.z)