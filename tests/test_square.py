"""Triangle tests."""

import math
import pytest


def test_square__constrained_angles(problem, tolerances):
    """Square."""
    SOLVE_TOL, TEST_ATOL = tolerances

    problem.add_line("l1", (0, 0), (1, 0))
    problem.add_line("l2", problem["l1"].end, (1, 1))
    problem.add_line("l3", problem["l2"].end, (1.5, 0.75))
    problem.add_line("l4", problem["l3"].end, problem["l1"].start)

    problem.constrain_line_length("l1", 1)
    problem.constrain_line_length("l2", 1)
    problem.constrain_line_length("l3", 1)
    problem.constrain_line_length("l4", 1)
    problem.constrain_angle_between_lines("l1", "l2", -90)
    problem.constrain_angle_between_lines("l2", "l3", -90)
    problem.constrain_angle_between_lines("l3", "l4", -90)

    problem.solve(tol=SOLVE_TOL)

    assert problem.error() == pytest.approx(0, abs=TEST_ATOL)
    assert problem["l1"].length() == pytest.approx(1, abs=TEST_ATOL)
    assert problem["l2"].length() == pytest.approx(1, abs=TEST_ATOL)
    assert problem["l3"].length() == pytest.approx(1, abs=TEST_ATOL)
    assert problem["l4"].length() == pytest.approx(1, abs=TEST_ATOL)
    assert problem["l1"].angle_to(problem["l2"]) == pytest.approx(-90, abs=TEST_ATOL)
    assert problem["l2"].angle_to(problem["l3"]) == pytest.approx(-90, abs=TEST_ATOL)
    assert problem["l3"].angle_to(problem["l4"]) == pytest.approx(-90, abs=TEST_ATOL)
    assert problem["l4"].angle_to(problem["l1"]) == pytest.approx(-90, abs=TEST_ATOL)
