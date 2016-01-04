from __future__ import division

import abc
import numpy as np
import operator

from parameters import Parameter

"""Geometry classes."""

class Primitive(object):
    """Abstract class representing a primitive shape."""

    __metaclass__ = abc.ABCMeta

    points = None
    """Points associated with this primitive."""

    name = None
    """Name of this primitive."""

    def __init__(self, points, name):
        """Constructs a new primitive.

        A list of points making up this primitive and a textual description
        must be specified.

        :param points: list of :class:`pygeosolve.geometry.Point` objects \
        associated with this primitive
        :param name: name of this primitive
        """

        self.points = points
        self.name = name

    def __str__(self):
        """String representation of this primitive.

        Returns a description of the :class:`~pygeosolve.geometry.Primitive` and
        a list of its associated :class:`~pygeosolve.geometry.Point` objects.

        :return: description of this :class:`~pygeosolve.geometry.Primitive` and
        its :class:`~pygeosolve.geometry.Point` objects
        """

        return "{0} with points {1}".format(self.name, ", ".join([str(point) for point in self.points]))

    @property
    def fixed(self):
        return reduce(operator.and_, [point.fixed for point in self.points])

    @fixed.setter
    def fixed(self, fixed):
        # set fixed status
        [setattr(point, 'fixed', fixed) for point in self.points]

class Point(Primitive):
    """Represents a two-dimensional point in Euclidean space."""

    x = None
    """The x-coordinate of this point."""

    y = None
    """The y-coordinate of this point."""

    def __init__(self, x, y):
        """Constructs a new point.

        :param x: x-position
        :param y: y-position
        """

        # set positions
        self.x = x
        self.y = y

        # call parent with self
        super(Point, self).__init__([self], "Point")

    def params(self):
        """Parameters associated with this problem.

        :return: list of :class:`~pygeosolve.parameters.Parameter` objects
        """

        # list of parameters
        return [self.x, self.y]

    def abs(self):
        return np.sqrt(np.power(self.x, 2) + np.power(self.y, 2))

    def __sub__(self, obj):
        return Point(self.x.value - obj.x.value, self.y.value - obj.y.value)

    @property
    def fixed(self):
        return self.x.fixed and self.y.fixed

    @fixed.setter
    def fixed(self, fixed):
        self.x.fixed = fixed
        self.y.fixed = fixed

    def __str__(self):
        """String representation of this point.

        :return: string representing (x, y) coordinates
        """

        return "({0}, {1})".format(self.x, self.y)

class Line(Primitive):
    """Represents a line formed between two points in Euclidean space."""

    def __init__(self, x1, y1, x2, y2):
        """Constructs a new Line object.

        :param x1: start x-coordinate
        :param y1: start y-coordinate
        :param x2: end x-coordinate
        :param y2: end y-coordinate
        """

        # start point
        start = Point(Parameter(x1), Parameter(y1))

        # end point
        end = Point(Parameter(x2), Parameter(y2))

        # call parent with start and end points
        super(Line, self).__init__([start, end], "Line")

    def start(self):
        """Line start point.

        :return: start :class:`~pygeosolve.geometry.Point` of \
        :class:`~pygeosolve.geometry.Line`
        """

        # first point represents the start
        return self.points[0]

    def end(self):
        """Line end point.

        :return: end :class:`~pygeosolve.geometry.Point` of \
        :class:`~pygeosolve.geometry.Line`
        """

        # second point represents the end
        return self.points[1]

    def dx(self):
        """Difference in length between end and start x-values.

        :return: difference in x-values
        """

        # subtract start x-coordinate from end x-coordinate
        return self.end().x.value - self.start().x.value

    def dy(self):
        """Difference in length between end and start y-values.

        :return: difference in y-values
        """

        # subtract start y-coordinate from end y-coordinate
        return self.end().y.value - self.start().y.value

    def hypot(self):
        """Length of line hypotenuse of triangle formed by the x- and
        y-coordinates of the start and end points. This represents the actual
        length of the line.

        :return: length of line
        """

        # Pythagoras' theorem
        return np.sqrt(self.dx() * self.dx() + self.dy() * self.dy())
