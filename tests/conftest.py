"""Shared fixtures."""

import pytest
from pygeosolve import Problem


@pytest.fixture
def problem():
    return Problem()


@pytest.fixture
def tolerance():
    """Tolerance for comparisons."""
    return 1e-3
