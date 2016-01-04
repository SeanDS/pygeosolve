from __future__ import division

import random
from pygeosolve.geometry import Line
from pygeosolve.constraints import LineLengthConstraint, AngularConstraint

"""pygeosolve object factory classes."""

class GeometryFactory(object):
    """Provides methods to produce new geometrical objects."""

    minimum_coordinate = -1000
    """Minimum possible coordinate"""

    maximum_coordinate = 1000
    """Maximum possible coordinate"""

    @classmethod
    def random_line(cls):
        """Generates a random line.

        :return: a :class:`~pygeosolve.geometry.Line` with random coordinates
        """
        return Line(*cls.random_coordinates(4))

    @classmethod
    def random_coordinate(cls):
        """Generates a random coordinate.

        :return: a random coordinate
        """

        return random.uniform(cls.minimum_coordinate, cls.maximum_coordinate)

    @classmethod
    def random_coordinates(cls, n, *args, **kwargs):
        """Generates n random coordinates.

        :param n: number of coordinates to generate
        :return: n random coordinates
        """

        return [cls.random_coordinate(*args, **kwargs) for _ in range(n)]

class ConstraintFactory(object):
    """Provides methods to produce new constraints between geometrical objects."""

    minimum_length = 0.001
    """Minimum possible length constraint"""

    maximum_length = 1000
    """Maximum possible length constraint"""

    @classmethod
    def random_length_constraint(cls, problem, line):
        """Generates a random length constraint on the specified line.

        :param problem: the :class:`~pygeosolve.problem.Problem` object to use
        :param line: the :class:`~pygeosolve.geometry.Line` object to set the \
        length constraint for
        :return: generated constraint length
        """

        # generate a random length
        length = cls.random_length()

        # add the random length constraint
        problem.add_constraint(LineLengthConstraint(line, length))

        return length

    @classmethod
    def random_angular_constraint(cls, problem, line_a, line_b):
        """Generates a random angular constraint between the specified lines.

        :param problem: the :class:`~pygeosolve.problem.Problem` object to use
        :param line_a: the first :class:`~pygeosolve.geometry.Line` object to \
        set the length constraint for
        :param line_b: the second :class:`~pygeosolve.geometry.Line` object to \
        set the length constraint for
        :return: generated constraint angle
        """

        # generate a random angle
        angle = cls.random_angle()

        # add the random anglular constraint
        problem.add_constraint(AngularConstraint(line_a, line_b, angle))

        return angle

    @classmethod
    def random_length(cls):
        """Generates a random length.

        :return: random length
        """

        return random.uniform(cls.minimum_length, cls.maximum_length)

    @classmethod
    def random_angle(cls):
        """Generates a random angle.

        :return: random angle
        """

        return random.uniform(0, 360)
