#!/usr/bin/env python3
"""Module defining a Square class that inherits from Rectangle."""
Rectangle = __import__('2-rectangle').Rectangle


class Square(Rectangle):
    """A class that represents a square."""

    def __init__(self, size):
        """Initialize a new Square."""
        self.integer_validator("size", size)
        self.__size = size
        super().__init__(size, size)

    def area(self):
        """Return the area of the square."""
        return self.__size * self.__size
