"""Triangle tests."""

import math
import pytest
from pygeosolve import Line
from . import SOLVE_TOL, TEST_ATOL


def test_triangle__right_to_equilateral(problem):
    """Right angled triangle constrained to be equilateral."""
    line1 = Line("l1", (0, 0), (1, 0))
    line2 = Line("l2", line1.end, (1, 1))
    line3 = Line("l3", line2.end, line1.start)

    problem.constrain_line_length(line1, 1)
    problem.constrain_line_length(line2, 1)
    problem.constrain_line_length(line3, 1)

    problem.solve(tol=SOLVE_TOL)

    assert problem.error() == pytest.approx(0, abs=TEST_ATOL)
    assert line1.angle_to(line2) == pytest.approx(120, abs=TEST_ATOL)
    assert line2.angle_to(line3) == pytest.approx(120, abs=TEST_ATOL)


def test_triangle__equilateral_to_right(problem):
    """Equilateral triangle constrained to be right."""
    line1 = Line("l1", (0, 0), (1, 0))
    line2 = Line("l2", line1.end, (0.5, math.sqrt(3) / 2))
    line3 = Line("l3", line2.end, line1.start)

    line1.fixed = True
    problem.constrain_line_length(line2, 1)
    problem.constrain_angle_between_lines(line1, line2, -90)

    problem.solve(tol=SOLVE_TOL)

    assert problem.error() == pytest.approx(0, abs=TEST_ATOL)
    assert line1.angle_to(line2) == pytest.approx(-90, abs=TEST_ATOL)
    assert line2.angle_to(line3) == pytest.approx(-135, abs=TEST_ATOL)
