#!/usr/bin/env python3
"""Module defining a BaseGeometry class."""


class BaseGeometry:
    """A class that represents base geometry."""

    def area(self):
        """Raise an exception indicating area is not implemented."""
        raise Exception("area() is not implemented")

    def integer_validator(self, name, value):
        """Validate that value is a positive integer."""
        if not isinstance(value, int):
            raise TypeError("{} must be an integer".format(name))
        if value <= 0:
            raise ValueError("{} must be greater than 0".format(name))
