"""Triangle tests."""

import pytest
from pygeosolve.geometry import Line


@pytest.mark.parametrize(
    "p1,p2,p3,p4,angle",
    (
        ((0, 0), (1, 0), (0, 0), (1, 0), 0),
        ((0, 0), (1, 0), (0, 0), (1, -1), 45),
        ((0, 0), (1, 0), (0, 0), (0, -1), 90),
        ((0, 0), (1, 0), (0, 0), (-1, -1), 135),
        ((0, 0), (1, 0), (0, 0), (0, 1), -90),
        ((0, 0), (1, 0), (1, 0), (0, 0), -180),
        ((0, 0), (1, 0), (0, 0), (-1, 1), -135),
    )
)
def test_line_angles(p1, p2, p3, p4, angle):
    l1 = Line("l1", p1, p2)
    l2 = Line("l2", p3, p4)
    assert l1.angle_to(l2) == pytest.approx(angle)
