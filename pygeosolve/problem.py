"""Constraint problems."""

import warnings
from functools import cached_property
from scipy.optimize import basinhopping
from .geometry import Point, Line, Invalid
from .constraints import LineLengthConstraint, LineAngleConstraint

# Indent size.
INDENT = " " * 4


class Problem:
    def __init__(self):
        self.primitives = {}
        self.constraints = []
        self.fixed_points = set()
        self._param_id_map = {}
        self._id_param_map = {}

    def __getitem__(self, item):
        try:
            return self.primitives[item]
        except KeyError:
            raise ValueError(f"{repr(item)} is not part of this problem")

    def add_point(self, *args, **kwargs):
        self._add(Point(*args, **kwargs))

    def add_line(self, *args, **kwargs):
        self._add(Line(*args, **kwargs))

    def _add(self, primitive):
        if primitive.name in self.primitives:
            raise ValueError(f"{repr(primitive.name)} already in problem")

        self.primitives[primitive.name] = primitive

    @cached_property
    def points(self):
        points = set()

        for primitive in self.primitives.values():
            points.update(primitive.points)

        return points

    @cached_property
    def free_params(self):
        """Free parameter names in this problem."""
        params = set()

        for point in self.points:
            for param_index in range(len(point.params)):
                name = self._param_to_id(point, param_index)
                if name not in self.fixed_points:
                    params.add(name)

        return params

    @property
    def free_values(self):
        values = []

        for name in self.free_params:
            point, param_index = self._id_to_param(name)
            values.append(point.params[param_index])

        return values

    def _param_to_id(self, point, param_index):
        key = point, param_index
        if key not in self._param_id_map:
            name = f"{repr(point)}#{param_index}"
            self._param_id_map[key] = name
            self._id_param_map[name] = key

        return self._param_id_map[key]

    def _id_to_param(self, name):
        return self._id_param_map[name]

    def _invalidate_caches(self):
        def invalidate(attrib):
            try:
                delattr(self, attrib)
            except AttributeError:
                pass

        for attrib in ("points", "free_params"):
            invalidate(attrib)

        self._param_id_map.clear()
        self._id_param_map.clear()

    def validate(self):
        """Validate the problem.

        This checks that primitives in the problem are valid, e.g. that lines have
        nonzero length.
        """
        status = [primitive.validate() for primitive in self.primitives.values()]
        invalid = list(filter(lambda s: isinstance(s, Invalid), status))

        if invalid:
            invalid_str = ", ".join(str(s) for s in invalid)
            raise ValueError(f"The following primitives are invalid: {invalid_str}")

    def constrain_position(self, name):
        """Fix the current position of a primitive.

        Parameters
        ----------
        name : :class:`str`
            The name of the primitive to fix.
        """
        for point in self[name].points:
            for param_index in range(len(point.params)):
                name = self._param_to_id(point, param_index)
                self.fixed_points.add(name)

    def constrain_line_length(self, name, length):
        """Add a constraint on the length of a line.

        Parameters
        ----------
        name : :class:`str`
            The name of the line to constrain.

        length : :class:`float`
            The line length to target.
        """
        self.constraints.append(LineLengthConstraint(self[name], length))

    def constrain_angle_between_lines(self, line_a, line_b, angle):
        """Add a constraint on the angle between two lines.

        Parameters
        ----------
        line_a, line_b : :class:`str`
            The names of the lines to constrain.

        :class:`float`
            The angle (in degrees) to target.
        """
        self.constraints.append(LineAngleConstraint(self[line_a], self[line_b], angle))

    def _update(self, values):
        """Update current free parameter values."""
        for name, value in zip(self.free_params, values):
            point, param_index = self._id_to_param(name)
            point.params[param_index] = value

    def error(self):
        """Calculate the current free parameter values' total error.

        Returns
        -------
        :class:`float`
            The total error.
        """
        return sum(constraint.error() for constraint in self.constraints)

    def solve(self, **kwargs):
        """Solve the problem.

        This attempts to minimise the error function given the defined constraints. A
        successful minimisation results in the new, optimised parameter values being
        assigned.

        Other Parameters
        ----------------
        kwargs
            Keyword arguments supported by :meth:`scipy.optimize.basinhopping`.

        Returns
        -------
        :class:`scipy.optimize.OptimizeResult`
            The optimisation result.
        """

        def f(x, *_):
            self._update(x)
            return self.error()

        self._invalidate_caches()
        self.validate()

        # Perform optimisation, or, if there's an error, restore the original solution.
        xpre = self.free_values
        try:
            solution = basinhopping(f, x0=self.free_values, **kwargs)
        except:
            self._update(xpre)
            raise

        if not solution.success:
            warnings.warn("Unable to find solution")
        else:
            self._update(solution.x)

        return solution

    def __str__(self):
        primitivestrs = []
        for primitive in self.primitives.values():
            primitivestrs.append(str(primitive))

        constraintstrs = []
        for constraint in self.constraints:
            constraintstrs.append(str(constraint))

        chunks = (
            f"Problem with {len(self.free_params)} free parameter(s):",
            f"\n{INDENT}" + f"\n{INDENT}".join(primitivestrs),
            "\n",
            f"and {len(self.constraints)} constraint(s):",
            f"\n{INDENT}" + f"\n{INDENT}".join(constraintstrs),
            "\n",
            f"\n{INDENT}Total error: {self.error()}"
        )

        return "".join(chunks)

    def plot(self, show=True):
        from .plot import plot_problem, show as show_problem

        plot_problem(self)

        if show:
            show_problem()
