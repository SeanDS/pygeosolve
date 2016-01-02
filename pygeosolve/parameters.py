from __future__ import division

import numpy as np

"""Parameter classes."""

class Parameter(object):
    """Represents a parameter that can be variable or fixed."""

    value = None
    """The value of this parameter."""

    fixed = False
    """Whether this parameter is fixed or not."""

    def __init__(self, value):
        """Constructs a new Parameter object.

        :param value: the initial value of this parameter
        """

        # set value
        self.value = value

    def __str__(self):
        """String representation of this parameter.

        :return: textual representation of the value of this parameter.
        """

        return str(self.value)
