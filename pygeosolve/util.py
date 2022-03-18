"""Utilities."""


def map_angle_about_zero(angle):
    """Map angle to be in the range (-180, 180]°."""
    return (angle + 180) % (360) - 180
