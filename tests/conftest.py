"""Shared fixtures."""

import pytest
from pygeosolve import Problem


@pytest.fixture
def problem():
    return Problem()
