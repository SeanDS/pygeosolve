"""Utilities."""


def map_angle_about_zero(angle):
    """Map angle to be in the range (-180, 180]°."""
    angle %= 360
    if angle > 180:
        angle -= 360
    return angle
