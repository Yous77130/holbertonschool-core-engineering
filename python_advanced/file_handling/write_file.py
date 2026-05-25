#!/usr/bin/env python3
"""Module for writing text to a file."""


def write_file(filename="", text=""):
    """Write a string to a text file and return number of characters written.

    Args:
        filename: path to the file to write
        text: string to write to the file

    Returns:
        Number of characters written
    """
    with open(filename, "w", encoding="utf-8") as f:
        return f.write(text)
