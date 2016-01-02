from __future__ import division

import numpy as np
import scipy.optimize as opt
import imp

import geometry
import plot

"""Problem classes"""

class Problem(object):
    params = []
    """Parameters associated with this problem."""

    constraints = []
    """Constraints associated with this problem."""

    error_calc_count = 0
    """Number of times this problem's error has been calculated."""

    def add_constraint(self, constraint):
        """Adds a constraint to this problem.

        :param constraint: the \
        :class:`~pygeosolve.constraints.AbstractConstraint` to add
        """

        # add constraint
        self.constraints.append(constraint)

        # extract its parameters
        self._add_constraint_params(constraint)

    def _add_param(self, param):
        """Adds a parameter to this problem.

        :param param: the :class:`~pygeosolve.parameters.Parameter` to add
        """

        # add parameter
        self.params.append(param)

    def _add_constraint_params(self, constraint):
        """Adds the parameters from a constraint to this problem.

        :param constraint: the \
        :class:`~pygeosolve.constraints.AbstractConstraint` to extract the \
        parameters from
        """

        # loop over the constraint's parameters
        for param in constraint.params:
            # check if parameter already exists in list
            if param not in self.params:
                # add parameter
                self._add_param(param)

    def free_params(self):
        """Non-fixed parameters associated with this problem.

        :return: list of free :class:`~pygeosolve.parameters.Parameter` objects
        """

        # empty list of free parameters
        free = []

        # loop over this problem's parameters
        for param in self.params:
            # identify free parameters
            if not param.fixed:
                # add to list
                free.append(param)

        return free

    def free_param_vals(self):
        """Values of non-fixed parameters associated with this problem.

        :return: list of free :class:`~pygeosolve.parameters.Parameter` values
        """

        # return values extracted from list of free parameters
        return np.array([param.value for param in self.free_params()])

    def _set_free_param_vals(self, values):
        """Sets values of non-fixed parameters in this problem.

        :param values: list of new values to set, in the same order as the \
        free parameters returned by `free_param_vals`
        """

        # loop over free parameters and the new values
        for param, value in zip(self.free_params(), values):
            # set the new value of this parameter
            param.value = value

    def error(self):
        """Calculates the total error associated with this problem.

        :return: total of individual \
        :class:`~pygeosolve.constraints.AbstractConstraint` errors"""

        # calculate error sum
        error = sum([constraint.error() for constraint in self.constraints])

        # increment error calculation count
        self.error_calc_count += 1

        return error

    def _error_with_vals(self, vals):
        """Sets new free parameter values and returns the new error.

        :param vals: the new free parameter values to set"""

        # set free parameter values
        self._set_free_param_vals(vals)

        # return new error
        return self.error()

    def solve(self):
        """Solves the problem.

        This method attempts to minimise the error function given the
        constraints defined within the problem. A successful minimisation
        results in the new, optimised parameter values being assigned."""

        # first guess at solution - just use current values
        x0 = self.free_param_vals()

        # call optimisation routine
        self.solution = opt.minimize(self._error_with_vals, x0)

        # update parameters from solution
        self.update()

    def solution_exists(self):
        """Checks if a solution has been computed.

        :return: True if solution exists, otherwise False"""

        return self.solution is not None

    def update(self):
        """Updates the list of free parameters associated with this problem.

        This method retrieves the values from the optimisation result and
        updates each one's corresponding parameter."""

        # check if solution exists
        if not self.solution_exists():
            # cannot update values without a solution
            raise Exception("Solution has not been computed")

        # update values from the optimisation result's solution
        self._set_free_param_vals(self.solution.x)

    def plot(self):
        """Plots the problem with its current values.

        Requires the PyQt4 module."""

        # try to find PyQt4 module
        try:
            imp.find_module("PyQt4")
        except ImportError:
            raise Exception("The PyQt4 module is required for plotting")

        # create canvas
        canvas = plot.Canvas()

        # empty list of lines added to canvas
        lines = []

        # add lines to canvas
        # TODO: add support for different primitives
        for constraint in self.constraints:
            for primitive in constraint.primitives:
                if isinstance(primitive, geometry.Line):
                    canvas.addLine(primitive)

        # show canvas
        canvas.show()

    def __str__(self):
        """String representation of this problem.

        :return: description of problem"""

        # build list of parameter string representations
        param_str = "\n\t" + "\n\t".join([str(param) for param in self.params])

        # return description
        return "Problem with parameters:{0}".format(param_str)
