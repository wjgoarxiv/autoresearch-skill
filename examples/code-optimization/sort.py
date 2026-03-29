#!/usr/bin/env python3
"""Sorting function -- the file the agent modifies."""


def sort_integers(arr: list[int]) -> list[int]:
    """In-place sort using list.sort() -- avoids copy overhead of sorted()."""
    arr = arr[:]  # copy to avoid mutating input (benchmark passes fresh copy anyway)
    arr.sort()
    return arr
