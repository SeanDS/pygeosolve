from __future__ import division

import math

"""Useful functions."""

def angle_between(line_a, line_b):
    """Calculates the angle between two lines.

    :param line_a: the first :class:`~pygeosolve.geometry.Line`
    :param line_b: the second :class:`~pygeosolve.geometry.Line`
    :return: angle (in degrees) between line_a and line_b
    """

    # TODO: add function to Line to extract angle
    return math.degrees(math.atan2(line_b.dy(), line_b.dx()) \
    - math.atan2(line_a.dy(), line_a.dx())) % 360
