# Research: Sorting Algorithm Optimization

## Goal
Reduce execution time of the integer sorting function in `sort.py` when sorting an array of 1,000,000 random integers. The function must produce a correctly sorted output and maintain sort stability.

## Success Metric
- **Metric:** Execution time in seconds (median of 5 runs on 1M random integers, range 0--10,000,000)
- **Target:** < 0.5s
- **Direction:** minimize

## Constraints
- **Max iterations:** 20
- **Time budget per experiment:** 5 minutes
- **Pause for review every:** never
- **Evaluator:** `python benchmark.py`
- **Keep policy:** score_improvement
- Pure Python only -- no C extensions, no Cython, no ctypes, no subprocess calls to compiled code
- Must maintain sort stability (equal elements preserve original order)
- Must handle edge cases: empty list, single element, already sorted, reverse sorted
- Function signature must remain: `def sort_integers(arr: list[int]) -> list[int]`
- No external libraries (only Python stdlib)

## Current Approach
Basic recursive quicksort implementation in `sort.py`:

```python
def sort_integers(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return sort_integers(left) + middle + sort_integers(right)
```

Baseline: 2.3991s median on 1M integers.

Known issues:
- Three list comprehensions create excessive temporary lists
- Recursive calls add stack overhead
- No special handling for nearly-sorted data
- Not stable (quicksort is inherently unstable, though this partition-based variant happens to be)

## Search Space
- **Allowed changes:** Algorithm choice, data structures, partitioning strategy, hybrid approaches, insertion sort cutoff for small subarrays, iterative vs recursive, built-in function usage (sorted() is allowed since it's stdlib)
- **Forbidden changes:** Function signature, input/output format, constraints above (pure Python, stability, edge cases)

## Context & References
- Python's built-in `sorted()` uses Timsort -- highly optimized C implementation, typically ~0.18s for 1M integers
- Using `sorted()` is allowed but the goal is to learn what algorithmic choices matter
- Timsort: hybrid merge sort + insertion sort, exploits existing order ("runs")
- Radix sort is O(n*k) but not comparison-based -- may be worth exploring for integers
- Insertion sort is fastest for small arrays (n < 20-50)

---

## History
<!-- Auto-maintained by the agent. Do not edit manually. -->
| # | Change | Metric | vs Baseline | Result | Timestamp |
|---|--------|--------|-------------|--------|-----------|
| 0 | Baseline: recursive quicksort with list comprehensions | 2.3991s | -- | -- | 2026-03-29 |
| 1 | Radix sort (LSD, base 256) | 0.8709s | -63.7% | KEPT | 2026-03-29 |
| 2 | Radix sort (LSD, base 65536) | 0.5727s | -76.1% | KEPT | 2026-03-29 |
| 3 | Micro-optimized radix (unrolled passes, local vars) | 0.4979s | -79.2% | KEPT | 2026-03-29 |
| 4 | Counting sort (range 0-10M) | 0.6717s | -72.0% | REVERTED | 2026-03-29 |
| 5 | array module for count arrays | 0.6967s | -71.0% | REVERTED | 2026-03-29 |
| 6 | Pre-computed dual histograms in single pass | 0.4486s | -81.3% | KEPT | 2026-03-29 |
| 7 | Radix base 2048 (11-bit, 3 passes) | 0.7205s | -70.0% | REVERTED | 2026-03-29 |
| 8 | sorted()-based radix (2 passes with C-level Timsort) | 0.4226s | -82.4% | KEPT | 2026-03-29 |
| 9 | Direct sorted() -- C Timsort | 0.192s | -92.0% | KEPT | 2026-03-29 |
| 10 | list.sort() in-place with copy | 0.1847s | -92.3% | KEPT | 2026-03-29 |
| 11 | Hybrid bucket(256)+Timsort | 0.2494s | -89.6% | REVERTED | 2026-03-29 |
