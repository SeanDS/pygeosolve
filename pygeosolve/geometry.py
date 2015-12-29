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
        :throws ValueError: if specified x is not a Parameter object
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
        :throws ValueError: if specified y is not a Parameter object
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
    """
    Abstract class representing a primitive shape.
    """
    
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, points, description):
        """
        Constructs a new primitive shape. A list of points making up this primitive and a textual description must be specified.
        """
        
        self.points = points
        self.description = description
    
    @property
    def points(self):
        """
        Points getter.
        
        :return: list of Point objects contained in this Primitive
        """
        
        return self._points
    
    @points.setter
    def points(self, points):
        """
        Points setter.
        
        :param points: list of Point objects
        """
        
        self._points = points
    
    def __str__(self):
        """
        String representation of this Primitive. Returns a description of the primitive and a list of its points.
        
        :return: description of this primitive
        """
        
        return "{0} with points {1}".format(self.description, ", ".join([str(point) for point in self.points]))

class Line(Primitive):
    """
    Represents a line formed between two points in Euclidean space.
    """
    
    def __init__(self, x1, y1, x2, y2):
        """
        Constructs a new Line object.
        
        :param x1: start x-coordinate
        :param y1: start y-coordinate
        :param x2: end x-coordinate
        :param y2: end y-coordinate
        """
        
        # call parent constructor with new Point objects for the start and end points.
        super(Line, self).__init__([Point(Parameter(x1), Parameter(y1)), Point(Parameter(x2), Parameter(y2))], "Line")
    
    @property
    def start(self):
        """
        Start point getter.
        
        :return: start Point object
        """
        
        # first parameter provided in list of points in constructor represents the start
        return self.points[0]
    
    @property
    def end(self):
        """
        End point getter.
        
        :return: end Point object
        """
        
        # second parameter provided in list of points in constructor represents the end
        return self.points[1]
    
    def dx(self):
        """
        Length of line along the x-axis.
        
        :return: x-axis length
        """
        
        # subtract start x-coordinate from end x-coordinate
        return self.end.x.value - self.start.x.value
    
    def dy(self):
        """
        Length of line along the y-axis.
        
        :return: y-axis length
        """
        
        # subtract start y-coordinate from end y-coordinate
        return self.end.y.value - self.start.y.value
    
    def hypot(self):
        """
        Length of line hypotenuse of triangle formed by the x- and y-coordinates of the start and end points.
        This represents the actual length of the line.
        
        :return: length of line
        """
        
        # Pythagoras' theorem
        return np.sqrt(self.dx() * self.dx() + self.dy() * self.dy())