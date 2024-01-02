"""Utility module for directional operations."""


def right(d):
    """Return the direction to the right of the given direction ('N', 'E',
    'S', or 'W'). """
    return "NESW"[("NESW".index(d) + 1) % 4]


def reverse(d):
    """Return the opposite direction of the given direction ('N', 'E', 'S',
    or 'W'). """
    return "NESW"[("NESW".index(d) + 2) % 4]


def left(d):
    """Return the direction to the left of the given direction ('N', 'E',
    'S', or 'W'). """
    return "NESW"[("NESW".index(d) + 3) % 4]
