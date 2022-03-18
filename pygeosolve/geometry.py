"""Geometry."""

import abc
from decimal import DivisionByZero
import numpy as np
from .util import map_angle_about_zero


class Primitive(metaclass=abc.ABCMeta):
    """A primitive shape.

    Parameters
    ----------
    name : :class:`str`
        The name.

    points : sequence
        The points that make up the primitive.
    """

    def __init__(self, name, points):
        self.name = name

        for i, point in enumerate(points):
            if not isinstance(point, Point):
                points[i] = Point(f"__{self.name}_p{i}__", *point)

        # Quick check that names are unique.
        assert len(set(p.name for p in points)) == len(points)

        self.points = points

    @abc.abstractmethod
    def __str__(self):
        raise NotImplementedError

    def __repr__(self):
        return f"<{self.__class__.__name__}@{hex(id(self))}>"

    def validate(self):
        return True


class Point(Primitive):
    """A 2D point in Euclidean space.

    Normally points should not be instantiated directly, but via :class:`primitives
    <.Primitive>`.

    Parameters
    ----------
    name : :class:`str`
        The name of this point.

    x, y : :class:`float`
        The x and y coordinates.
    """

    def __init__(self, name, x, y):
        super().__init__(name, [self])
        self.params = [x, y]

    @property
    def x(self):
        return self.params[0]

    @property
    def y(self):
        return self.params[1]

    def norm(self):
        return np.sqrt(np.power(self.x, 2) + np.power(self.y, 2))

    def __add__(self, other):
        return self.__class__(
            self._op_name("+", other), self.x + other.x, self.y + other.y
        )

    def __sub__(self, other):
        return self.__class__(
            self._op_name("-", other), self.x - other.x, self.y - other.y
        )

    def __str__(self):
        return f"{self.__class__.__name__}({self.name}, ({self.x}, {self.y}))"

    def _op_name(self, op, other):
        return f"{self}{op}{other}"


class Line(Primitive):
    """A line formed between two 2D points in Euclidean space.

    Parameters
    ----------
    start, end : :class:`tuple` containg two :class:`floats <float>` or
                 :class:`points <.Point>`
    """

    def __init__(self, name, start, end):
        super().__init__(name, [start, end])

    @property
    def start(self):
        return self.points[0]

    @property
    def end(self):
        return self.points[1]

    def dx(self):
        """The difference between the end and start x-coordinates.

        Returns
        -------
        :class:`float`
            The difference.
        """
        return self.end.x - self.start.x

    def dy(self):
        """The difference between the end and start y-coordinates.

        Returns
        -------
        :class:`float`
            The difference.
        """
        return self.end.y - self.start.y

    def length(self):
        """The line length.

        Returns
        -------
        :class:`float`
            The length.
        """
        return (self.end - self.start).norm()

    def angle(self):
        """The angle of the vector formed by this line translated to the origin.

        Returns
        -------
        :class:`float`
            The angle, in degrees, in the range (-180, 180].
        """
        angle = np.degrees(np.arctan2(self.dx(), self.dy()))
        return map_angle_about_zero(angle)

    def angle_to(self, other):
        """The angle to other line with respect to this one.

        The angle is defined as the clockwise rotation from the direction of `self` to
        get to the direction of `other`.

        Parameters
        ----------
        other : :class:`.Line`
            The other line.

        Returns
        -------
        :class:`float`
            The angle, in degrees, in the range (-180, 180].
        """
        dot = self.dx() * other.dx() + self.dy() * other.dy()
        det = self.dy() * other.dx() - self.dx() * other.dy()
        angle = np.degrees(np.arctan2(det, dot))

        return map_angle_about_zero(angle)

    def validate(self):
        zerolength = np.isclose(self.length(), 0)

        if zerolength:
            return Invalid(self, "zero length")

        return True

    def __str__(self):
        points = ", ".join(str(point) for point in self.points)
        return (
            f"{self.__class__.__name__}({self.name}, [{points}], "
            f"length={self.length()}, angle={self.angle()})"
        )


class Invalid:
    def __init__(self, primitive, reason):
        self.primitive = primitive
        self.reason = reason

    def __str__(self):
        return f"{self.primitive} ({self.reason})"
