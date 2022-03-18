"""Make a right triangle equilateral."""

from pygeosolve import Problem

# Create problem with initial line positions.
problem = Problem()
problem.add_line("a", (0, 0), (10, 0))
problem.add_line("b", problem["a"].end, (10, 10))
problem.add_line("c", problem["b"].end, problem["a"].start)

# Constrain the lines.
problem.constrain_position("a")
problem.constrain_line_length("b", 10)
problem.constrain_line_length("c", 10)

# Solve
problem.solve()

# Print the current solution state.
print(problem)

# Plot the solved sketch.
problem.plot()
