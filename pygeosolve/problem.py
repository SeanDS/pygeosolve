from __future__ import division

import numpy as np
import scipy.optimize as opt
import operator
import imp

import geometry
import plot

class Problem(object):
    def __init__(self):
        self._params = []
        self._constraints = []
        self.errorCalcCount = 0
        
    def __str__(self):
        paramStr = "\n\t" + "\n\t".join([str(param) for param in self.params])
        
        return "Problem with parameters:{0}".format(paramStr)
    
    @property
    def params(self):
        return self._params
    
    @params.setter
    def params(self, params):
        self._params = params
    
    def addParam(self, param):
        self.params.append(param)
        
    @property
    def freeParams(self):
        free = []
        
        for param in self.params:
            if not param.fixed:
                free.append(param)
        
        return free
    
    def freeParamVals(self):
        return np.array([param.value for param in self.freeParams])
    
    def setFreeParamVals(self, values):
        for param, value in zip(self.freeParams, values):
            param.value = value
    
    @property
    def constraints(self):
        return self._constraints
    
    def addConstraint(self, constraint):
        self._constraints.append(constraint)
        
        self.addConstraintParams(constraint)
    
    def addConstraintParams(self, constraint):
        for param in constraint.params:
            if param not in self.params:
                self.addParam(param)
    
    def errorForVals(self, vals):
        self.setFreeParamVals(vals)
        
        return self.error()
    
    def error(self):
        """
        Calculate total error
        """
        
        return reduce(operator.add, [constraint.error() for constraint in self.constraints])
    
    def solve(self):
        # first guess at solution - just use current values
        x0 = self.freeParamVals()
        
        # optimise
        self.solution = opt.minimize(self.errorForVals, x0)
        
        # update parameters from solution
        self.update()
    
    def update(self):
        if not isinstance(self.solution, opt.OptimizeResult):
            raise Exception("Solution is not yet computed or is invalid")
        
        self.setFreeParamVals(self.solution.x)
    
    def plot(self):
        # try to find PyQt4 module
        try:
            imp.find_module("PyQt4")
        except ImportError:
            raise Exception("The PyQt4 module is required for plotting")
        
        # create canvas
        canvas = plot.Canvas()
        
        # lines added to canvas
        lines = []
        
        # add lines
        for constraint in self.constraints:
            for primitive in constraint.primitives:
                if isinstance(primitive, geometry.Line):
                    canvas.addLine(primitive)
        
        canvas.show()