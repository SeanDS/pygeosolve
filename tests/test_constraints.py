import unittest
import random
import pygeosolve.tools as tools
from pygeosolve.geometry import Line
from pygeosolve.problem import Problem
from pygeosolve.constraints import LineLengthConstraint, AngularConstraint
from object_factory import GeometryFactory, ConstraintFactory

"""Constraint tests."""

class TestConstraints(unittest.TestCase):
    """Tests the solver for various constraints."""

    problem = None
    """Problem object."""

    line_a = None
    """First line."""

    line_b = None
    """Second line."""

    def setUp(self):
        """Sets up the problem."""

        # new problem object
        self.problem = Problem()

        # new random lines
        self.line_a = GeometryFactory.random_line()
        self.line_b = GeometryFactory.random_line()

    def test_angular_constraint(self):
        """Sets up an angular constraint, solves it and checks it."""

        # fix first line
        self.line_a.fixed = True

        # create length constraint
        length_b = ConstraintFactory.random_length_constraint(self.problem, \
        self.line_b)

        # create angular constraint
        angle = ConstraintFactory.random_angular_constraint(self.problem, \
        self.line_a, self.line_b)

        # solve
        self.problem.solve()
        print self.problem.solution

        print "A: ({0}, {1})".format(self.line_a.dx(), self.line_a.dy())
        print "B: ({0}, {1})".format(self.line_b.dx(), self.line_b.dy())

        print angle, tools.angle_between(self.line_a, self.line_b)

        self.problem.plot(False)

        ###
        # check solution

        # get angle between lines
        actual_angle = tools.angle_between(self.line_a, self.line_b)

        # check
        self.assertEqual(angle, actual_angle)

if __name__ == '__main__':
    unittest.main()
