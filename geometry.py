from __future__ import division

import abc
import numpy as np
import numbers

from parameters import Parameter

"""
Geometry classes.
"""

class Point(object):
    """
    Represents a two-dimensional point in Euclidean space.
    """
    
    def __init__(self, x, y):
        """
        Constructs a new Point object.
        
        :param x: x-position
        :param y: y-position
        """
        
        # set positions
        self.x = x
        self.y = y
    
    @property
    def x(self):
        """
        x-position getter.
        
        :return: Parameter object representing x-position
        """
        
        return self._x
    
    @x.setter
    def x(self, x):
        """
        x-position setter.
        
        :param x: Parameter object representing x-position
        :raise ValueError: if specified x is not a Parameter object
        """
        
        if not isinstance(x, Parameter):
            raise ValueError("Specified x must be a Parameter object")
        
        # set x
        self._x = x

    @property
    def y(self):
        """
        y-position getter.
        
        :return: Parameter object representing y-position
        """
        
        return self._y
    
    @y.setter
    def y(self, y):
        """
        y-position setter.
        
        :param y: Parameter object representing y-position
        :raise ValueError: if specified y is not a Parameter object
        """
        
        if not isinstance(y, Parameter):
            raise ValueError("Specified y must be a Parameter object")
        
        # set y
        self._y = y
    
    def params(self):
        """
        Returns a list containing the Parameter objects representing x- and y-positions.
        
        :return: list containing the Parameter objects
        """
        
        # list of Parameter objects
        return [self.x, self.y]
    
    def __str__(self):
        """
        String representation of this Point object.
        
        :return: string representing (x, y) coordinates
        """
        
        return "({0}, {1})".format(self.x, self.y)

class Primitive(object):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, points, description):
        self.points = points
        self.description = description
    
    @property
    def points(self):
        return self._points
    
    @points.setter
    def points(self, points):
        self._points = points
    
    def __str__(self):
        return "{0} with points {1}".format(self.description, ", ".join([str(point) for point in self.points]))

class Line(Primitive):
    def __init__(self, x1, y1, x2, y2):        
        super(Line, self).__init__([Point(Parameter(x1), Parameter(y1)), Point(Parameter(x2), Parameter(y2))], "Line")
    
    @property
    def start(self):
        return self.points[0]
    
    @property
    def end(self):
        return self.points[1]
    
    def dx(self):
        return self.end.x.value - self.start.x.value
    
    def dy(self):
        return self.end.y.value - self.start.y.value
    
    def hypot(self):
        return np.sqrt(self.dx() * self.dx() + self.dy() * self.dy())