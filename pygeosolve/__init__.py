"""Geometric constraint solver."""

# Get package version.
try:
    from ._version import version as __version__
except ImportError:
    raise FileNotFoundError("Could not find _version.py. Ensure you have run setup.")


from .problem import Problem

__all__ = ("__version__", "Problem")
