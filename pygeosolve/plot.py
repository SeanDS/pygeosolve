"""Plotting."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc


try:
    from itertools import pairwise
except ImportError:
    # Must be Python < 3.10.
    from itertools import tee

    def pairwise(iterable):
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)


def plot_problem(problem):
    fig = plt.figure()
    ax = fig.gca()
    ax.set_aspect("equal", "datalim")

    for primitive in problem.primitives.values():
        for point in primitive.points:
            ax.plot(point.x, point.y, marker="x", color="red")

        for p1, p2 in pairwise(primitive.points):
            ax.plot([p1.x, p2.x], [p1.y, p2.y], color="blue")
            ax.text(p1.x + (p2.x - p1.x) / 2, p1.y + (p2.y - p1.y) / 2, primitive.name)


def show():
    plt.show()
