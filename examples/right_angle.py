from pygeosolve.geometry import Line
from pygeosolve.problem import Problem
from pygeosolve.constraints import LineLengthConstraint, AngularConstraint, \
PointToPointDistanceConstraint

# create lines with correct lengths but incorrect angle
line_a = Line(30, 0, 0, 0)
line_b = Line(30, 0, 0, 0)

# create problem
problem = Problem()

###
# constraints

# length constraints
problem.add_constraint(LineLengthConstraint(line_a, 30))
problem.add_constraint(LineLengthConstraint(line_b, 30))

# fix corner to be 90 degrees
problem.add_constraint(AngularConstraint(line_a, line_b, 90))
problem.add_constraint(PointToPointDistanceConstraint(line_a.end(), \
line_b.start(), 0))

# fix line_a so it doesn't move
line_a.fixed = True

# solve
problem.solve()
print problem.solution

# plot
problem.plot()
