"""Constraints."""

import abc
import numpy as np
from .util import map_angle_about_zero


class Constraint(metaclass=abc.ABCMeta):
    """A constraint between primitives.

    A constraint is defined between one or more :class:`.Primitive` objects. This class
    defines the interface for concrete constraints to determine their error in the
    current problem using these primitives.

    Parameters
    ----------
    primitives : sequence
        The primitives associated with this constraint.
    """

    def __init__(self, primitives):
        self.primitives = primitives

    @property
    def points(self):
        """The points associated with the primitives associated with this constraint."""

        points = []
        for primitive in self.primitives:
            points.extend(primitive.points)

        return points

    @property
    def params(self):
        """The parameters associated with the points within this constraint."""

        params = set()
        for point in self.points:
            params.update(point.params)

        return params

    @abc.abstractmethod
    def value(self):
        """The current value of the constrained parameter(s)."""
        raise NotImplementedError

    @abc.abstractmethod
    def error(self):
        """The error function for this constraint."""
        raise NotImplementedError

    def __str__(self):
        return f"{self.__class__.__name__}(current={self.value()}, error={self.error()})"

    def __repr__(self):
        return f"<{self.__class__.__name__}@{hex(id(self))}>"


class LineLengthConstraint(Constraint):
    """Constraint on the length of a line.

    Parameters
    ----------
    line : :class:`.Line`
        The line to constrain.

    length : :class:`float`
        The length to constrain the line to.
    """

    def __init__(self, line, length):
        super().__init__([line])
        self._length = None
        self.length = length

    @property
    def length(self):
        """The constraint length."""
        return self._length

    @length.setter
    def length(self, length):
        if length < 0:
            raise ValueError("length must be >= 0")

        self._length = length

    @property
    def line(self):
        return self.primitives[0]

    def value(self):
        """The current value of the constrained parameter(s)."""
        return self.line.length()

    def error(self):
        """The current length constraint error.

        Returns
        -------
        :class:`float`
            The error.
        """
        # The difference in length.
        return np.abs(self.value() - self.length) ** 2


class LineAngleConstraint(Constraint):
    """Constraint on the angle between two lines.

    Parameters
    ----------
    line_a, line_b : :class:`.Line`
        The lines to constrain.

    angle : :class:`float`
        The angle (in degrees) to constrain the lines to.
    """

    def __init__(self, line_a, line_b, angle):
        super().__init__([line_a, line_b])
        self._angle = None
        self.angle = angle

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        self._angle = map_angle_about_zero(angle)

    @property
    def line_a(self):
        return self.primitives[0]

    @property
    def line_b(self):
        return self.primitives[1]

    def value(self):
        """The current value of the constrained parameter(s)."""
        return self.line_a.angle_to(self.line_b)

    def error(self):
        """The current angle constraint error.

        Returns
        -------
        :class:`float`
            The error.
        """
        return np.abs((self.value() - self.angle) / self.angle) ** 2


class PointToPointDistanceConstraint(Constraint):
    """Constraint on the distance between two points.

    Parameters
    ----------
    point_a, point_b : :class:`.Point`
        The points to constrain.

    distance : :class:`float`
        The distance to constrain the points' separation to.
    """

    def __init__(self, point_a, point_b, distance):
        super().__init__([point_a, point_b])
        self.distance = distance

    @property
    def point_a(self):
        return self.primitives[0]

    @property
    def point_b(self):
        return self.primitives[1]

    def error(self):
        """The current distance constraint error.

        Returns
        -------
        :class:`float`
            The error.
        """
        return np.abs((self.point_a - self.point_b).norm() - self.distance)
