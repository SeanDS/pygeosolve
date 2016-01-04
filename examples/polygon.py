from pygeosolve.geometry import Line
from pygeosolve.problem import Problem
from pygeosolve.constraints import LineLengthConstraint, AngularConstraint, PointToPointDistanceConstraint

# create lines with approximately correct positions
line_a = Line(0, 0, 30, 0)
line_b = Line(30, 0, 30, 31)
line_c = Line(30, 31, -1, 29)
line_d = Line(-1, 29, 1, -1)

# create problem
problem = Problem()

###
# constraints

# length constraint for line_a
problem.add_constraint(LineLengthConstraint(line_a, 30))

# angular and point-to-point constraints at each corner
problem.add_constraint(AngularConstraint(line_a, line_b, 90))
problem.add_constraint(PointToPointDistanceConstraint(line_a.end(), \
line_b.start(), 0))
problem.add_constraint(AngularConstraint(line_b, line_c, 90))
problem.add_constraint(PointToPointDistanceConstraint(line_b.end(), \
line_c.start(), 0))
problem.add_constraint(AngularConstraint(line_c, line_d, 90))
problem.add_constraint(PointToPointDistanceConstraint(line_c.end(), \
line_d.start(), 0))
problem.add_constraint(AngularConstraint(line_d, line_a, 90))
problem.add_constraint(PointToPointDistanceConstraint(line_d.end(), \
line_a.start(), 0))

# solve
problem.solve()
print problem.solution

# print angles between lines
import pygeosolve.tools as tools
print tools.angle_between(line_a, line_b)
print tools.angle_between(line_b, line_c)
print tools.angle_between(line_c, line_d)
print tools.angle_between(line_d, line_a)

# plot
problem.plot()
