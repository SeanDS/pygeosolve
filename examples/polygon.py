"""Make a polygon into a square."""

from pygeosolve import Problem

# Create problem with initial line positions.
problem = Problem()
problem.add_line("a", (0, 0), (30, 0))
problem.add_line("b", problem["a"].end, (30, 31))
problem.add_line("c", problem["b"].end, (-1, 29))
problem.add_line("d", problem["c"].end, problem["a"].start)

# Constrain the lines.
problem.constrain_position("a")
problem.constrain_line_length("b", 30)
problem.constrain_angle_between_lines("a", "b", -90)
problem.constrain_angle_between_lines("b", "c", -90)
problem.constrain_angle_between_lines("c", "d", -90)
problem.constrain_angle_between_lines("d", "a", -90)

# Solve
problem.solve()

# Print the current solution state.
print(problem)

# Plot the solved sketch.
problem.plot()
