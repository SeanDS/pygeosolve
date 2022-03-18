"""Triangle tests."""

import math
import pytest


def test_triangle__right_to_equilateral(problem, tolerance):
    """Right angled triangle constrained to be equilateral."""
    problem.add_line("l1", (0, 0), (1, 0))
    problem.add_line("l2", problem["l1"].end, (1, 1))
    problem.add_line("l3", problem["l2"].end, problem["l1"].start)

    problem.constrain_line_length("l1", 1)
    problem.constrain_line_length("l2", 1)
    problem.constrain_line_length("l3", 1)

    result = problem.solve()

    assert result.success
    # There are two solutions to the problem, with +120° or -120° angles between lines.
    assert abs(problem["l1"].angle_to(problem["l2"])) == pytest.approx(120, abs=tolerance)
    assert abs(problem["l2"].angle_to(problem["l3"])) == pytest.approx(120, abs=tolerance)


def test_triangle__equilateral_to_right(problem, tolerance):
    """Equilateral triangle constrained to be right."""
    problem.add_line("l1", (0, 0), (1, 0))
    problem.add_line("l2", problem["l1"].end, (0.5, math.sqrt(3) / 2))
    problem.add_line("l3", problem["l2"].end, problem["l1"].start)

    problem.constrain_position("l1")
    problem.constrain_line_length("l2", 1)
    problem.constrain_angle_between_lines("l1", "l2", -90)

    result = problem.solve()

    assert result.success
    assert problem["l1"].angle_to(problem["l2"]) == pytest.approx(-90, abs=tolerance)
    assert problem["l2"].angle_to(problem["l3"]) == pytest.approx(-135, abs=tolerance)



def test_square__constrained_angles(problem, tolerance):
    """Square."""
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

    result = problem.solve()

    assert result.success
    assert problem["l1"].length() == pytest.approx(1, abs=tolerance)
    assert problem["l2"].length() == pytest.approx(1, abs=tolerance)
    assert problem["l3"].length() == pytest.approx(1, abs=tolerance)
    assert problem["l4"].length() == pytest.approx(1, abs=tolerance)
    assert problem["l1"].angle_to(problem["l2"]) == pytest.approx(-90, abs=tolerance)
    assert problem["l2"].angle_to(problem["l3"]) == pytest.approx(-90, abs=tolerance)
    assert problem["l3"].angle_to(problem["l4"]) == pytest.approx(-90, abs=tolerance)
    assert problem["l4"].angle_to(problem["l1"]) == pytest.approx(-90, abs=tolerance)
