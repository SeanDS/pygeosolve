from __future__ import division

import numpy as np
import numbers
import types

"""
Parameter classes.
"""

class Parameter(object):
    """
    Represents a parameter that can be variable or fixed.
    """
    
    def __init__(self, value):
        """
        Constructs a new Parameter object.
        
        :param value: the initial value of this parameter
        """
        
        # set value
        self.value = value
        
        # by default not fixed
        self.fixed = False
    
    def __str__(self):
        """
        String representation of this parameter.
        
        :return: textual representation of the value of this parameter.
        """
        
        return str(self.value)
    
    @property
    def value(self):
        """
        Property representing the value of this :class:`~pygeosolve.parameters.Parameter`.
        
        :getter: returns the value of this :class:`~pygeosolve.parameters.Parameter`
        :setter: sets the value of this :class:`~pygeosolve.parameters.Parameter`
        :type: number
        
        :return: value of parameter
        """
        
        return self._value
    
    @value.setter
    def value(self, value):
        """
        Value setter.
        
        :raises ValueError: if value is not a number.
        """
        
        # check that value is a number
        if not isinstance(value, numbers.Number):
            raise ValueError("Specified value parameter is not a number")
        
        self._value = value
        
    @property
    def fixed(self):
        """
        Property representing whether this :class:`~pygeosolve.parameters.Parameter` is fixed (`True`), i.e. it cannot be changed in the solution, or not (`False`)
        
        :getter: returns the fixed status of this :class:`~pygeosolve.parameters.Parameter`
        :setter: sets the fixed status of this :class:`~pygeosolve.parameters.Parameter`
        :type: boolean
        """
        
        return self._fixed
    
    @fixed.setter
    def fixed(self, fixed):
        """
        Fixed setter.
        
        :raises ValueError: if fixed is not :class:`types.BooleanType`
        """
        
        if not isinstance(fixed, types.BooleanType):
            raise ValueError("Specified fixed value is not boolean")
        
        # set fixed value
        self._fixed = fixed