"""Shared fixtures."""

import pytest
from pygeosolve import Problem


@pytest.fixture
def problem():
    return Problem()


@pytest.fixture
def tolerances():
    """Tolerances for solving and comparisons."""
    SOLVE_TOL = 1e-6
    TEST_ATOL = 1e-3  # Solve tolerance uses square of errors, so this needs to be lower.
    return SOLVE_TOL, TEST_ATOL
