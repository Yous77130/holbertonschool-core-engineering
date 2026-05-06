#!/usr/bin/env python3


def pow(a, b):
    result = 1
    if b >= 0:
        for i in range(b):
            result *= a
    else:
        for i in range(-b):
            result *= a
        result = 1 / result
    return result
