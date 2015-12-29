from __future__ import division

import numpy as np
import scipy.optimize as opt
import operator
import imp

import geometry
import plot

class Problem(object):
    def __init__(self):
        self.params = []
        self.constraints = []
        self.error_calc_count = 0
        
    def add_constraint(self, constraint):
        self.constraints.append(constraint)
        
        self._add_constraint_params(constraint)
    
    def _add_param(self, param):
        self.params.append(param)
    
    def _add_constraint_params(self, constraint):
        for param in constraint.params:
            if param not in self.params:
                self._add_param(param)
        
    def free_params(self):
        free = []
        
        for param in self.params:
            if not param.fixed:
                free.append(param)
        
        return free
    
    def free_param_vals(self):
        return np.array([param.value for param in self.free_params()])
    
    def _set_free_param_vals(self, values):
        for param, value in zip(self.free_params(), values):
            param.value = value
    
    def error(self):
        """
        Calculate total error
        """
        
        # calculate error
        error = reduce(operator.add, [constraint.error() for constraint in self.constraints])
        
        # increment count
        self.error_calc_count += 1
        
        return error

    def _error_with_vals(self, vals):
        self._set_free_param_vals(vals)
        
        return self.error()
    
    def solve(self):
        # first guess at solution - just use current values
        x0 = self.free_param_vals()
        
        # optimise
        self.solution = opt.minimize(self._error_with_vals, x0)
        
        # update parameters from solution
        self.update()
    
    def update(self):
        if not isinstance(self.solution, opt.OptimizeResult):
            raise Exception("Solution is not yet computed or is invalid")
        
        self._set_free_param_vals(self.solution.x)
    
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
        
    def __str__(self):
        param_str = "\n\t" + "\n\t".join([str(param) for param in self.params])
        
        return "Problem with parameters:{0}".format(param_str)