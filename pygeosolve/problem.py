"""Constraint problems."""

from multiprocessing.sharedctypes import Value
import warnings
from functools import cached_property
from contextlib import contextmanager
from scipy.optimize import minimize
from .geometry import Invalid
from .constraints import LineLengthConstraint, LineAngleConstraint


class Problem:
    def __init__(self):
        self.constraints = []

    @cached_property
    def params(self):
        params = []

        for constraint in self.constraints:
            for param in constraint.params:
                if param not in params:
                    params.append(param)

        return params

    @cached_property
    def free_params(self):
        free = []

        for param in self.params:
            if not param.fixed and param not in free:
                free.append(param)

        return free

    @cached_property
    def free_values(self):
        """Current values of the free parameters in this problem.

        Returns
        -------
        :class:`list`
            The current free parameter values.
        """
        return [param.value for param in self.free_params]

    @cached_property
    def primitives(self):
        primitives = []

        for constraint in self.constraints:
            for primitive in constraint.primitives:
                if primitive not in primitives:
                    primitives.append(primitive)
        
        return primitives

    def _invalidate_caches(self):
        def invalidate(attrib):
            try:
                delattr(self, attrib)
            except AttributeError:
                pass
        
        for attrib in ("params", "free_params", "free_values", "primitives"):
            invalidate(attrib)

    def _validate_primitives(self):
        status = [primitive.validate() for primitive in self.primitives]
        invalid = list(filter(lambda s: isinstance(s, Invalid), status))

        if invalid:
            raise ValueError(
                f"The following primitives are invalid: {', '.join(str(s) for s in invalid)}"
            )


    def constrain_line_length(self, line, length):
        """Add a constraint on the length of a line.

        Parameters
        ----------
        line : :class:`.Line`
            The line to constrain.
        
        length : :class:`float`
            The line length to target.
        """
        self.constraints.append(LineLengthConstraint(line, length))

    def constrain_angle_between_lines(self, line_a, line_b, angle):
        """Add a constraint on the angle between two lines.

        Parameters
        ----------
        line_a, line_b : :class:`.Line`
            The lines to constrain.
        
        :class:`float`
            The angle (in degrees) to target.
        """
        self.constraints.append(LineAngleConstraint(line_a, line_b, angle))

    def _update(self, values):
        """Update current free parameter values."""
        for param, value in zip(self.free_params, values):
            param.value = value

    def error(self):
        """Calculate the current free parameter values' total error.

        Returns
        -------
        :class:`float`
            The total error.
        """
        return sum(constraint.error() for constraint in self.constraints)

    def solve(self):
        """Solves the problem.

        This method attempts to minimise the error function given the
        constraints defined within the problem. A successful minimisation
        results in the new, optimised parameter values being assigned.
        """

        def f(x, *_):
            self._update(x)
            return self.error()

        self._invalidate_caches()
        self._validate_primitives()

        # Perform optimisation, or, if there's an error, restore the original solution.
        with self._temporary_parameters():
            solution = minimize(
                f,
                x0=self.free_values,
                method="COBYLA"
            )

        if not solution.success:
            warnings.warn("Unable to find solution")
        else:
            self._update(solution.x)

    @contextmanager
    def _temporary_parameters(self):
        xpre = self.free_values
        yield
        self._update(xpre)

    def __str__(self):        
        constraintstrs = []
        for constraint in self.constraints:
            constraintstrs.append(str(constraint))

        chunks = (
            f"Problem with {len(self.free_params)} free parameter(s) and {len(self.constraints)} constraint(s)",
            "\n\t" + "\n\t".join(constraintstrs),
            f"\nTotal error: {self.error()}"
        )

        return "".join(chunks)
