#!/usr/bin/env python3
"""Module for reading a file and printing its content."""


def read_file(filename=""):
    """Read a text file and print its content to stdout.

    Args:
        filename: path to the file to read
    """
    with open(filename, encoding="utf-8") as f:
        print(f.read(), end="")
