from __future__ import division

import abc
import numpy as np

from geometry import *

class AbstractConstraint(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, primitives, *args, **kwargs):
        self.primitives = primitives
    
    @property
    def primitives(self):
        return self._primitives
    
    @primitives.setter
    def primitives(self, primitives):
        self._primitives = primitives
    
    @abc.abstractmethod
    def error(self):
        pass
    
    @property
    @abc.abstractmethod
    def points(self):
        pass
    
    @property
    def params(self):
        params = []
        
        for point in self.points:
            if point.x not in params:
                params.append(point.x)
            
            if point.y not in params:
                params.append(point.y)
        
        return params

class LengthConstraint(AbstractConstraint):
    def __init__(self, line, length, *args, **kwargs):
        super(LengthConstraint, self).__init__([line], *args, **kwargs)
        
        self.length = length
    
    def error(self):
        dLength = self.line.hypot() - self.length
        
        return dLength * dLength * 100
    
    @property
    def line(self):
        return self.primitives[0]
    
    @property
    def points(self):
        return self.line.points

class AngularConstraint(AbstractConstraint):
    def __init__(self, lineA, lineB, angle, *args, **kwargs):
        super(AngularConstraint, self).__init__([lineA, lineB], *args, **kwargs)
        
        self.angle = angle
    
    def error(self):        
        # hypotenuse of each line
        hypotA = self.lineA.hypot()
        hypotB = self.lineB.hypot()
        
        # x-axis projection scaled by hypotenuse
        xProjA = self.lineA.dx() / hypotA
        xProjB = self.lineB.dx() / hypotB
        
        # y-axis projection scaled by hypotenuse
        yProjA = self.lineA.dy() / hypotA
        yProjB = self.lineB.dy() / hypotB
        
        # sum of products of projections along each axis
        projSum = xProjA * xProjB + yProjA * yProjB
        
        # angular error
        angError = projSum + np.cos(np.radians(self.angle))
        
        # return square
        return angError * angError
    
    @property
    def lineA(self):
        return self.primitives[0]
    
    @property
    def lineB(self):
        return self.primitives[1]
    
    @property
    def points(self):
        return self.lineA.points + self.lineB.points