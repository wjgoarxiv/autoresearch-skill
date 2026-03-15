"""Sorting function under optimization. Only this file gets modified by the research loop."""


def sort_integers(arr: list[int]) -> list[int]:
    """Sort a list of integers in ascending order via LSD radix sort (base 65536).

    Iteration 6 result: 0.7513s median on 1M integers (-68.7% vs baseline).
    """
    a = list(arr)
    n = len(a)
    if n <= 1:
        return a

    # Handle negative numbers by offsetting
    min_val = min(a)
    if min_val < 0:
        a = [x - min_val for x in a]

    max_val = max(a)
    if max_val == 0:
        if min_val < 0:
            return [x + min_val for x in a]
        return a

    # LSD radix sort, base 65536 (2 passes for values up to ~4 billion)
    BITS = 16
    MASK = (1 << BITS) - 1
    b = [0] * n

    shift = 0
    while (max_val >> shift) > 0:
        count = [0] * (MASK + 2)
        for x in a:
            count[((x >> shift) & MASK) + 1] += 1
        for i in range(1, len(count)):
            count[i] += count[i - 1]
        for x in a:
            digit = (x >> shift) & MASK
            b[count[digit]] = x
            count[digit] += 1
        a, b = b, a
        shift += BITS

    if min_val < 0:
        a = [x + min_val for x in a]
    return a
