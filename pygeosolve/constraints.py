from __future__ import division

import abc
import numpy as np
import operator

from geometry import Primitive, Line

"""Constraint classes."""

class AbstractConstraint(object):
    """Defines a most basic constraint.

    A constraint is defined between one or more
    :class:`~pygeosolve.geometry.Primitive` objects. This class defines the
    constructor to populate this constraint's associated
    :class:`~pygeosolve.geometry.Primitive` objects and abstract methods to
    calculate its error, access to primitive
    :class:`~pygeosolve.geometry.Point` objects and
    :class:`~pygeosolve.parameters.Parameter` objects.
    """

    __metaclass__ = abc.ABCMeta

    primitives = None
    """The primitives associated with this constraint"""

    def __init__(self, primitives):
        """Constructs a new constraint.

        :param primitives: list of :class:`~pygeosolve.geometry.Primitive` \
        objects associated with this constraint
        """

        self.primitives = primitives

    @abc.abstractmethod
    def error(self):
        """Abstract method to define the error function for this constraint."""

        pass

    @property
    def points(self):
        """The points associated with the primitives associated with this
        constraint.

        :return: a collection of :class:`~pygeosolve.geometry.Point` objects \
        contained within the :class:`~pygeosolve.geometry.Primitive` objects \
        defined as part of this \
        :class:`~pygeosolve.constraints.AbstractConstraint`
        """

        # extract lists of points for each primitive
        points = [primitive.points for primitive in self.primitives]

        # combine all points into one list and return
        return reduce(operator.add, points)

    @property
    def params(self):
        """The parameters associated with the points within this constraint.

        :return: a collection of :class:`~pygeosolve.parameters.Parameter` \
        objects contained within this constraint
        """

        # empty parameter list
        params = []

        # extract Parameter objects from points
        for point in self.points:
            if point.x not in params:
                params.append(point.x)

            if point.y not in params:
                params.append(point.y)

        return params

class LineLengthConstraint(AbstractConstraint):
    """Constrains the length of a line."""

    def __init__(self, line, length, *args, **kwargs):
        """Constructs a new length constraint.

        :param line: :class:`~pygeosolve.geometry.Line` primitive to be \
        constrained
        :param length: constraint length
        """

        # construct parent
        super(LineLengthConstraint, self).__init__([line], *args, **kwargs)

        # set length
        self.length = length

    @property
    def length(self):
        """The constraint length."""
        return self._length

    @length.setter
    def length(self, length):
        # cast length to float
        length = float(length)

        # check length is positive
        if length < 0:
            raise ValueError("Length must be >= 0")

        self._length = length

    @property
    def line(self):
        """The line primitive associated with this constraint."""

        # first and only primitive should be the line
        return self.primitives[0]

    def error(self):
        """Calculates length constraint error.

        :return: the error between the :class:`~pygeosolve.geometry.Line` \
        length versus :class:`~pygeosolve.constraints.LengthConstraint` length
        """

        # difference in length
        dl = self.line.hypot() - self.length

        # error: scaled square of length difference
        return dl * dl * 100

class AngularConstraint(AbstractConstraint):
    """Constrains the angle between two lines."""

    angle = None
    """The constraint angle."""

    def __init__(self, line_a, line_b, angle, *args, **kwargs):
        """Constructs a new angular constraint.

        :param line_a: first :class:`~pygeosolve.geometry.Line` primitive to \
        be constrained
        :param line_b: second :class:`~pygeosolve.geometry.Line` primitive to \
        be constrained
        :param angle: constraint angle (in degrees) between `line_a` and \
        `line_b`
        """

        # construct parent
        super(AngularConstraint, self).__init__([line_a, line_b], *args, **kwargs)

        # set angle
        self.angle = angle

    @property
    def line_a(self):
        """First line associated with this constraint.

        :return: the first :class:`~pygeosolve.geometry.Line` provided to the \
        constraint in its constructor
        """

        return self.primitives[0]

    @property
    def line_b(self):
        """Second line associated with this constraint.

        :return: the second :class:`~pygeosolve.geometry.Line` provided to the \
        constraint in its constructor
        """

        return self.primitives[1]

    def error(self):
        """Calculates angular constraint error.

        :return: the error of the actual angle versus the \
        :class:`~pygeosolve.constraints.AngularConstraint` angle"""

        # hypotenuse of each line
        hypot_a = self.line_a.hypot()
        hypot_b = self.line_b.hypot()

        # x-axis projection scaled by hypotenuse
        x_proj_a = self.line_a.dx() / hypot_a
        x_proj_b = self.line_b.dx() / hypot_b

        # y-axis projection scaled by hypotenuse
        y_proj_a = self.line_a.dy() / hypot_a
        y_proj_b = self.line_b.dy() / hypot_b

        # sum of products of projections along each axis
        proj_total = x_proj_a * x_proj_b + y_proj_a * y_proj_b

        # angular error
        error = proj_total + np.cos(np.radians(self.angle))

        # return square
        return error * error
