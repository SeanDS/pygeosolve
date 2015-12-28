from __future__ import division

import numpy as np

class Parameter(object):
    def __init__(self, value):
        self.value = value
        self.fixed = False
    
    def __str__(self):
        return str(self.value)
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):        
        self._value = value
        
    @property
    def fixed(self):
        return self._fixed
    
    @fixed.setter
    def fixed(self, fixed):
        self._fixed = fixed