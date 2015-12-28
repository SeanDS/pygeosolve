from geometry import Line
from problem import Problem
from constraints import LengthConstraint, AngularConstraint

lineA = Line(20, 20, 50, 40)
lineB = Line(50, 40, 20, 0)

problem = Problem()

problem.addConstraint(LengthConstraint(lineA, 30))
problem.addConstraint(LengthConstraint(lineB, 20))
problem.addConstraint(AngularConstraint(lineA, lineB, 90))

lineA.start.x.fixed = True
lineA.start.y.fixed = True
lineA.end.x.fixed = True
lineA.end.y.fixed = True

problem.solve()

print lineA
print lineB

print lineA.hypot()
print lineB.hypot()

print problem.solution

problem.plot()