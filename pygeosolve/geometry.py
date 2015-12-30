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
        Constructs a new point.
        
        :param x: x-position
        :param y: y-position
        """
        
        # set positions
        self.x = x
        self.y = y
    
    @property
    def x(self):
        """
        Property representing the x-coordinate of this :class:`~pygeosolve.geometry.Point`.
        
        :getter: returns the x-coordinate of this :class:`~pygeosolve.geometry.Point`
        :setter: sets the x-coordinate of this :class:`~pygeosolve.geometry.Point`
        :type: number
        """
        
        return self._x
    
    @x.setter
    def x(self, x):
        """
        x-position setter.
        
        :raises ValueError: if specified x is not of type :class:`~pygeosolve.parameters.Parameter`
        """
        
        if not isinstance(x, Parameter):
            raise ValueError("Specified x must be a Parameter object")
        
        # set x
        self._x = x

    @property
    def y(self):
        """
        Property representing the y-coordinate of this :class:`~pygeosolve.geometry.Point`.
        
        :getter: returns the y-coordinate of this :class:`~pygeosolve.geometry.Point`
        :setter: sets the y-coordinate of this :class:`~pygeosolve.geometry.Point`
        :type: number
        """
        
        return self._y
    
    @y.setter
    def y(self, y):
        """
        y-position setter.
        
        :raises ValueError: if specified y is not of type :class:`~pygeosolve.parameters.Parameter`
        """
        
        if not isinstance(y, Parameter):
            raise ValueError("Specified y must be a Parameter object")
        
        # set y
        self._y = y
    
    def params(self):
        """
        Returns a list containing the :class:`~pygeosolve.parameters.Parameter` objects representing x- and y-coordinates.
        
        :return: list containing the :class:`~pygeosolve.parameters.Parameter` objects
        :rtype: list
        """
        
        # list of :class:`~pygeosolve.parameters.Parameter` objects
        return [self.x, self.y]
    
    def __str__(self):
        """
        String representation of this :class:`~pygeosolve.geometry.Point`.
        
        :return: string representing (x, y) coordinates
        :rtype: string
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
        Points property.
        
        :getter: returns a list of :class:`~pygeosolve.geometry.Point` objects contained within this :class:`~pygeosolve.geometry.Primitive`
        :setter: sets the list of :class:`~pygeosolve.geometry.Point` objects contained within this :class:`~pygeosolve.geometry.Primitive`
        :type: list
        """
        
        return self._points
    
    @points.setter
    def points(self, points):
        """
        Points setter.
        
        :raises ValueError: if list contains any object not of type :class:`~pygeosolve.geometry.Point`
        """
        
        if not isinstance(points, list):
            raise ValueError("Specified points argument is not a list")
        
        for point in points:
            if not isinstance(point, Point):
                raise ValueError("The specified points list must contain only Point objects")
        
        # set points
        self._points = points
    
    def __str__(self):
        """
        String representation of this :class:`~pygeosolve.geometry.Primitive`. Returns a description of the :class:`~pygeosolve.geometry.Primitive` and a list of its associated :class:`~pygeosolve.geometry.Point` objects.
        
        :return: description of this :class:`~pygeosolve.geometry.Primitive` and its :class:`~pygeosolve.geometry.Point` objects
        :rtype: string
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
        
        # call parent constructor with new :class:`~pygeosolve.geometry.Point` objects for the start and end points.
        super(Line, self).__init__([Point(Parameter(x1), Parameter(y1)), Point(Parameter(x2), Parameter(y2))], "Line")
    
    def start(self):
        """
        Start point getter.
        
        :return: start of :class:`~pygeosolve.geometry.Line`
        :rtype: :class:`~pygeosolve.geometry.Point`
        """
        
        # first parameter provided in list of points in constructor represents the start
        return self.points[0]
    
    def end(self):
        """
        End point getter.
        
        :return: end of :class:`~pygeosolve.geometry.Line`
        :rtype: :class:`~pygeosolve.geometry.Point`
        """
        
        # second parameter provided in list of points in constructor represents the end
        return self.points[1]
    
    def dx(self):
        """
        Length of line along the x-axis.
        
        :return: x-axis length
        :rtype: positive number
        """
        
        # subtract start x-coordinate from end x-coordinate
        return self.end().x.value - self.start().x.value
    
    def dy(self):
        """
        Length of line along the y-axis.
        
        :return: y-axis length
        :rtype: positive number
        """
        
        # subtract start y-coordinate from end y-coordinate
        return self.end().y.value - self.start().y.value
    
    def hypot(self):
        """
        Length of line hypotenuse of triangle formed by the x- and y-coordinates of the start and end points.
        This represents the actual length of the line.
        
        :return: length of line
        :rtype: positive number
        """
        
        # Pythagoras' theorem
        return np.sqrt(self.dx() * self.dx() + self.dy() * self.dy())