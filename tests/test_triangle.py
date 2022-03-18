"""Triangle tests."""

import math
import pytest


def test_triangle__right_to_equilateral(problem, tolerances):
    """Right angled triangle constrained to be equilateral."""
    SOLVE_TOL, TEST_ATOL = tolerances

    problem.add_line("l1", (0, 0), (1, 0))
    problem.add_line("l2", problem["l1"].end, (1, 1))
    problem.add_line("l3", problem["l2"].end, problem["l1"].start)

    problem.constrain_line_length("l1", 1)
    problem.constrain_line_length("l2", 1)
    problem.constrain_line_length("l3", 1)

    problem.solve(tol=SOLVE_TOL)

    assert problem.error() == pytest.approx(0, abs=TEST_ATOL)
    assert problem["l1"].angle_to(problem["l2"]) == pytest.approx(120, abs=TEST_ATOL)
    assert problem["l2"].angle_to(problem["l3"]) == pytest.approx(120, abs=TEST_ATOL)


def test_triangle__equilateral_to_right(problem, tolerances):
    """Equilateral triangle constrained to be right."""
    SOLVE_TOL, TEST_ATOL = tolerances

    problem.add_line("l1", (0, 0), (1, 0))
    problem.add_line("l2", problem["l1"].end, (0.5, math.sqrt(3) / 2))
    problem.add_line("l3", problem["l2"].end, problem["l1"].start)

    problem.constrain_position("l1")
    problem.constrain_line_length("l2", 1)
    problem.constrain_angle_between_lines("l1", "l2", -90)

    problem.solve(tol=SOLVE_TOL)

    assert problem.error() == pytest.approx(0, abs=TEST_ATOL)
    assert problem["l1"].angle_to(problem["l2"]) == pytest.approx(-90, abs=TEST_ATOL)
    assert problem["l2"].angle_to(problem["l3"]) == pytest.approx(-135, abs=TEST_ATOL)
