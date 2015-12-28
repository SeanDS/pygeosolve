from __future__ import division

import abc
import numpy as np
import collections
import numbers

from geometry import Primitive

"""
Constraint classes.
"""

class AbstractConstraint(object):
    """
    Defines a most basic constraint.
    
    A constraint is defined between one or more Primitive objects. This class
    defines the constructor to populate the Primitive objects and abstract
    methods to calculate the constraint's error, access to primitive points and
    parameters.
    """
    
    __metaclass__ = abc.ABCMeta

    def __init__(self, primitives):
        """
        Abstract constraint constructor.
        
        :param primitives: a Primitive object or iterable returning Primitive objects
        """
        
        self.primitives = primitives
    
    @property
    def primitives(self):
        """
        Primitives iterable getter method.
        
        :return: iterable returning Primitive objects within this constraint
        """
        
        return self._primitives
    
    @primitives.setter
    def primitives(self, primitives):
        """
        Primitives setter method.
        
        :param primitives: Primitive or iterable returning Primitive objects
        :raises ValueError: if primitives argument is not either a Primitive object or iterable containing Primitive objects
        """
        
        # check if specified primitives argument is iterable
        if not isinstance(primitives, collections.Iterable):
            # not an iterable, so let's make it one
            primitives = [primitives]
        
        # check contents of iterable
        for primitive in primitives:
            # check if this object is Primitive
            if not isinstance(primitive, Primitive):
                raise ValueError("Primitives argument must be a Primitive object or iterable containing thereof")
        
        # set it
        self._primitives = primitives
    
    @abc.abstractmethod
    def error(self):
        """
        Abstract method to define the error function for this constraint.
        """
        
        pass
    
    @property
    def points(self):
        """
        Returns a collection of points contained within the primitives
        defined as part of this constraint.
        
        :return: list of points
        """
        
        # extract lists of points from each primitive and add them to an overall list
        return reduce(lambda x, y: x + y, [primitive.points for primitive in self.primitives])
    
    @property
    def params(self):
        """
        Returns a list of Parameter objects contained within the constrained primitives of this constraint.
        
        :return: iterator that returns Parameter objects
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

class LengthConstraint(AbstractConstraint):
    """
    Constrains the length of a Line primitive.
    """
    
    def __init__(self, line, length, *args, **kwargs):
        """
        Constructs a new LengthConstraint object.
        
        :param line: Line primitive to be constrained
        :param length: constraint length
        """
        
        # construct parent
        super(LengthConstraint, self).__init__([line], *args, **kwargs)
        
        # set length
        self.length = length
    
    @property
    def length(self):
        """
        Length getter.
        
        :return: constraint length
        """
        
        return self._length
    
    @length.setter
    def length(self, length):
        """
        Length setter.
        
        :param length: Length constraint
        :raises ValueError: if length is not a positive real number
        """
        
        # check validity of specified length
        if not isinstance(length, numbers.Number) or length < 0:
            raise ValueError("Length must be a positive number")

        # set length
        self._length = length
        
    @property
    def line(self):
        """
        Line object getter.
        
        :return: Line object this constraint constrains
        """
        
        return self.primitives[0]
    
    def error(self):
        """
        Calculates error in actual line length versus constraint length.
        
        :return: error in length
        """
        
        # difference in length
        dLength = self.line.hypot() - self.length
        
        # error: scaled square of length difference
        return dLength * dLength * 100

class AngularConstraint(AbstractConstraint):
    """
    Constrains the angle between two Line primitives.
    """
    
    def __init__(self, lineA, lineB, angle, *args, **kwargs):
        """
        Constructs a new AngularConstraint object.
        
        :param lineA: first Line primitive to be constrained
        :param lineB: second Line primitive to be constrained
        :param angle: constraint angle in degrees between lineA and lineB
        """
        
        # construct parent
        super(AngularConstraint, self).__init__([lineA, lineB], *args, **kwargs)
        
        # set angle
        self.angle = angle
    
    @property
    def angle(self):
        """
        Angle getter.
        
        :return: constraint angle
        """
        
        return self._angle
    
    @angle.setter
    def angle(self, angle):
        """
        Angle setter.
        
        :param angle: angle in degrees to constrain
        :raises ValueError: if angle is not a real number
        """
        
        # check validity of specified angle
        if not isinstance(angle, numbers.Number):
            raise ValueError("Angle must be a real number")

        # set angle
        self._angle = angle
        
    @property
    def lineA(self):
        """
        First line getter.
        
        :return: Line primitive representing first line in constraint
        """
        
        return self.primitives[0]
    
    @property
    def lineB(self):
        """
        Second line getter.
        
        :return: Line primitive representing second line in constraint
        """
        
        return self.primitives[1]
    
    def error(self):
        """
        Calculates error in actual angle versus constraint angle.
        
        :return: error in angle
        """
        
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