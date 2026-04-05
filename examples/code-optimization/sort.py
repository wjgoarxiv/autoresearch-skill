#!/usr/bin/env python3
"""Sorting function -- the file the agent modifies."""


def sort_integers(arr: list[int]) -> list[int]:
    """Use CPython's built-in sorted() -- single-call, avoids explicit copy."""
    return sorted(arr)
