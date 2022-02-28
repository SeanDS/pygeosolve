"""Parameters."""


class Parameter:
    """A parameter.

    Parameters can be free or fixed.
    """
    def __init__(self, value, fixed=False):
        if isinstance(value, self.__class__):
            # Copy constructor.
            if fixed:
                raise ValueError(
                    f"Cannot define 'fixed' when passing an existing {self.__class__}."
                )
            fixed = value.fixed

        self.value = float(value)
        self.fixed = fixed

    def __str__(self):
        fixed = "fixed" if self.fixed else "free"
        return f"{self.__class__.__name__}({self.value}, {fixed})"

    def __add__(self, other):
        return self.__class__(self.value + getattr(other, "value", other))

    def __sub__(self, other):
        return self.__class__(self.value - getattr(other, "value", other))

    def __truediv__(self, other):
        return self.__class__(self.value / getattr(other, "value", other))

    def __float__(self):
        return self.value
