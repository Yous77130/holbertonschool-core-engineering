#!/usr/bin/env python3
"""Module defining a Rectangle class."""
BaseGeometry = __import__('base_geometry').BaseGeometry


class Rectangle(BaseGeometry):
    """A class that represents a rectangle."""

    def __init__(self, width, height):
        """Initialize a new Rectangle."""
        self.integer_validator("width", width)
        self.integer_validator("height", height)
        self.__width = width
        self.__height = height
