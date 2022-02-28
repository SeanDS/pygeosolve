"""Triangle tests."""

import math
import pytest
from pygeosolve import Line
from . import SOLVE_TOL, TEST_ATOL


def test_square__constrained_angles(problem):
    """Square."""
    line1 = Line("l1", (0, 0), (1, 0))
    line2 = Line("l2", line1.end, (1, 1))
    line3 = Line("l3", line2.end, (1.5, 0.75))
    line4 = Line("l4", line3.end, line1.start)

    problem.constrain_line_length(line1, 1)
    problem.constrain_line_length(line2, 1)
    problem.constrain_line_length(line3, 1)
    problem.constrain_line_length(line4, 1)
    problem.constrain_angle_between_lines(line1, line2, -90)
    problem.constrain_angle_between_lines(line2, line3, -90)
    problem.constrain_angle_between_lines(line3, line4, -90)

    problem.solve(tol=SOLVE_TOL)

    assert problem.error() == pytest.approx(0, abs=TEST_ATOL)
    assert line1.length() == pytest.approx(1, abs=TEST_ATOL)
    assert line2.length() == pytest.approx(1, abs=TEST_ATOL)
    assert line3.length() == pytest.approx(1, abs=TEST_ATOL)
    assert line4.length() == pytest.approx(1, abs=TEST_ATOL)
    assert line1.angle_to(line2) == pytest.approx(-90, abs=TEST_ATOL)
    assert line2.angle_to(line3) == pytest.approx(-90, abs=TEST_ATOL)
    assert line3.angle_to(line4) == pytest.approx(-90, abs=TEST_ATOL)
    assert line4.angle_to(line1) == pytest.approx(-90, abs=TEST_ATOL)
