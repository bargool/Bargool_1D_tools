class Point(object):
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z


class Vector(object):
    def __init__(self, **kwargs):
        if 'x' in kwargs and 'y' in kwargs and 'z' in kwargs:
            self._x = kwargs['x']
            self._y = kwargs['y']
            self._z = kwargs['z']
        elif 'p0' in kwargs and 'p1' in kwargs:
            p0 = kwargs['p0']
            p1 = kwargs['p1']
            self._x = p1.x - p0.x
            self._y = p1.y - p0.y
            self._z = p1.z - p0.z
        else:
            raise AttributeError

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z


class Line(object):
    def __init__(self, **kwargs):
        if 'point' in kwargs and 'vector' in kwargs:
            point = kwargs['point']
            vector = kwargs['vector']
            self._x0 = point.x
            self._y0 = point.y
            self._z0 = point.z
            self._p1 = vector.x
            self._p2 = vector.y
            self._p3 = vector.z
            self._vector = vector
        else:
            raise AttributeError

    @property
    def vector(self):
        return self._vector

    def get_point_on_line(self, x=None, y=None, z=None):
        assert len([i for i in (x, y, z) if i is not None]) == 1
        if x is not None:
            t = -1 * self._x0 / self._p1
        elif y is not None:
            t = -1 * self._y0 / self._p2
        else:  # z is not None
            t = -1 * self._z0 / self._p3
        return Point(
            x or self._p1 * t + self._x0,
            y or self._p2 * t + self._y0,
            z or self._p3 * t + self._z0
        )


class Plane(object):
    def __init__(self, **kwargs):
        if 'point' in kwargs and 'normal' in kwargs:
            point = kwargs['point']
            normal = kwargs['normal']
            self._a = normal.x
            self._b = normal.y
            self._c = normal.z
            self._d = -1 * (normal.x * point.x) - (normal.y * point.y) - (normal.z * point.z)
        elif 'point' in kwargs and 'vector1' in kwargs and 'vector2' in kwargs:
            p = kwargs['point']
            v = kwargs['vector1']
            w = kwargs['vector2']
            self._a = v.y*w.z - w.y * v.z
            self._b = w.x * v.z - v.x * w.z
            self._c = v.x * w.y - w.x * v.y
            self._d = (p.x * w.y * v.z + p.y * v.x * w.z + p.z * w.x * v.y -
                       p.x * v.y * w.z - p.y * w.x * v.z - p.z * v.x * w.y)
        else:
            raise AttributeError

    def intersect(self, plane):
        if not isinstance(plane, Plane):
            raise AttributeError
        x = self._b * plane._c - self._c * plane._b
        y = self._c * plane._a - self._a * plane._c
        z = self._a * plane._b - self._b * plane._a
        return Vector(x=x, y=y, z=z)

    def get_z(self, x, y):
        return (-1 * self._a * x - self._b * y - self._d) / self._c if self._c else 0


def create_slope_plane(point0, point1):
    """Creates slope plane that uses line threw point0, point1 as gradient"""

    # If points on same height - we need just horizontal plane
    if point0.z == point1.z:
        return Plane(point=point0, normal=Vector(x=0, y=0, z=1))

    # We are going to create plane that perpendicular to input line point0 - point1
    # Then we intersect it to plane XOY and retrieve line perpendicular to previous
    # With this two lines we create slope plane
    v = Vector(p0=point0, p1=point1)
    line1 = Line(point=point0, vector=v)
    intersect_point = line1.get_point_on_line(z=0)

    plane = Plane(point=intersect_point, normal=v)
    plane_xoy = Plane(point=intersect_point, normal=Vector(x=0, y=0, z=1))
    intersect_line = Line(point=intersect_point, vector=plane.intersect(plane_xoy))
    return Plane(point=intersect_point, vector1=v, vector2=intersect_line.vector)
