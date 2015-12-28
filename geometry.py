from __future__ import division

import abc
import numpy as np

from parameters import Parameter

class Point(object):
    def __init__(self, x, y):
        self.x = Parameter(x)
        self.y = Parameter(y)
    
    def params(self):
        return [self.x, self.y]
    
    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)

class CompoundPointObject(object):
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

class Line(CompoundPointObject):
    def __init__(self, x1, y1, x2, y2):        
        super(Line, self).__init__([Point(x1, y1), Point(x2, y2)], "Line")
    
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