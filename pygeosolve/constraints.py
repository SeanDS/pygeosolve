from __future__ import division

import abc
import numpy as np
import collections
import numbers

from geometry import Primitive, Line

"""
Constraint classes.
"""

class AbstractConstraint(object):
    """
    Defines a most basic constraint.
    
    A constraint is defined between one or more :class:`~pygeosolve.geometry.Primitive` objects. This class defines the constructor to populate this constraint's associated :class:`~pygeosolve.geometry.Primitive` objects and abstract methods to calculate its error, access to primitive :class:`~pygeosolve.geometry.Point` objects and :class:`~pygeosolve.parameters.Parameter` objects.
    """
    
    __metaclass__ = abc.ABCMeta

    def __init__(self, primitives):
        """
        Abstract constraint constructor.
        
        :param primitives: a :class:`~pygeosolve.geometry.Primitive` object or iterable returning :class:`~pygeosolve.geometry.Primitive` objects
        """
        
        self.primitives = primitives
    
    @abc.abstractmethod
    def error(self):
        """
        Abstract method to define the error function for this :class:`~pygeosolve.constraints.AbstractConstraint`.
        """
        
        pass
    
    @property
    def primitives(self):
        """
        Property representing the :class:`~pygeosolve.geometry.Primitive` objects contained within this :class:`~pygeosolve.constraints.AbstractConstraint`.
        
        :getter: returns a list containing the :class:`~pygeosolve.geometry.Primitive` objects attached to this :class:`~pygeosolve.constraints.AbstractConstraint`
        :setter: sets the list of :class:`~pygeosolve.geometry.Primitive` objects attached to this :class:`~pygeosolve.constraints.AbstractConstraint`
        :type: list
        """
        
        return self._primitives
    
    @primitives.setter
    def primitives(self, primitives):
        """
        Primitives setter method.
        
        :raises ValueError: if primitives argument is not either a :class:`~pygeosolve.geometry.Primitive` object or list containing :class:`~pygeosolve.geometry.Primitive` objects
        """
        
        # check if specified primitives argument is iterable
        if not isinstance(primitives, list):
            # not a list, so let's make it one
            primitives = [primitives]
        
        # check contents of list
        for primitive in primitives:
            # check if this object is :class:`~pygeosolve.geometry.Primitive`
            if not isinstance(primitive, Primitive):
                raise ValueError("Primitives argument must be a Primitive object or list containing thereof")
        
        # set it
        self._primitives = primitives
    
    @property
    def points(self):
        """
        Property representing a collection of :class:`~pygeosolve.geometry.Point` objects contained within the primitives
        defined as part of this :class:`~pygeosolve.constraints.AbstractConstraint`.
        
        :getter: returns a list of :class:`~pygeosolve.geometry.Point` objects associated with this :class:`~pygeosolve.constraints.AbstractConstraint`
        :type: list
        """
        
        # extract lists of points from each primitive and add them to an overall list
        return reduce(lambda x, y: x + y, [primitive.points for primitive in self.primitives])
    
    @property
    def params(self):
        """
        Property representing a collection of :class:`~pygeosolve.parameters.Parameter` objects contained within this :class:`~pygeosolve.constraints.AbstractConstraint`.
        
        :getter: returns a list of :class:`~pygeosolve.parameters.Parameter` objects associated with this :class:`~pygeosolve.constraints.AbstractConstraint`
        :type: list
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
    Constrains the length of a :class:`~pygeosolve.geometry.Line` primitive.
    """
    
    def __init__(self, line, length, *args, **kwargs):
        """
        Constructs a new length constraint.
        
        :param line: :class:`~pygeosolve.geometry.Line` primitive to be constrained
        :param length: constraint length
        :raises ValueError: if line is not of type :class:`~pygeosolve.geometry.Line`
        """
        
        # check type of line argument
        if not isinstance(line, Line):
            raise ValueError("Specified line is not of type Line")
        
        # construct parent
        super(LengthConstraint, self).__init__([line], *args, **kwargs)
        
        # set length
        self.length = length
    
    @property
    def length(self):
        """
        Property representing the length defined by this :class:`~pygeosolve.constraints.LengthConstraint`.
        
        :getter: returns the length constrained by this :class:`~pygeosolve.constraints.LengthConstraint`
        :setter: sets the length constrained by this :class:`~pygeosolve.constraints.LengthConstraint`
        :type: positive real number
        """
        
        return self._length
    
    @length.setter
    def length(self, length):
        """
        Length setter.
        
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
        Property representing the :class:`~pygeosolve.geometry.Line` object associated with this :class:`~pygeosolve.constraints.LengthConstraint`.
        
        :getter: returns the :class:`~pygeosolve.geometry.Line` object associated with this :class:`~pygeosolve.constraints.LengthConstraint`
        :type: :class:`~pygeosolve.geometry.Line`
        """
        
        return self.primitives[0]
    
    def error(self):
        """
        Calculates error in :class:`~pygeosolve.geometry.Line` length versus :class:`~pygeosolve.constraints.LengthConstraint` length.
        
        :return: error in length
        :rtype: number
        """
        
        # difference in length
        dl = self.line.hypot() - self.length
        
        # error: scaled square of length difference
        return dl * dl * 100

class AngularConstraint(AbstractConstraint):
    """
    Constrains the angle between two :class:`~pygeosolve.geometry.Line` primitives.
    """
    
    def __init__(self, line_a, line_b, angle, *args, **kwargs):
        """
        Constructs a new angular constraint.
        
        :param line_a: first :class:`~pygeosolve.geometry.Line` primitive to be constrained
        :param line_b: second :class:`~pygeosolve.geometry.Line` primitive to be constrained
        :param angle: constraint angle in degrees between line_a and line_b
        """
        
        # construct parent
        super(AngularConstraint, self).__init__([line_a, line_b], *args, **kwargs)
        
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
    def line_a(self):
        """
        First :class:`~pygeosolve.geometry.Line` getter.
        
        :return: :class:`~pygeosolve.geometry.Line` primitive representing first line in constraint
        """
        
        return self.primitives[0]
    
    @property
    def line_b(self):
        """
        Second :class:`~pygeosolve.geometry.Line` getter.
        
        :return: :class:`~pygeosolve.geometry.Line` primitive representing second line in constraint
        """
        
        return self.primitives[1]
    
    def error(self):
        """
        Calculates error in actual angle versus constraint angle.
        
        :return: error in angle
        """
        
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