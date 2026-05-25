#!/usr/bin/env python3
"""Module for appending text to a file."""


def append_write(filename="", text=""):
    """Append a string to a text file and return number of characters added.

    Args:
        filename: path to the file to append to
        text: string to append to the file

    Returns:
        Number of characters added
    """
    with open(filename, "a", encoding="utf-8") as f:
        return f.write(text)
