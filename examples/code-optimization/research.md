# Research: Sorting Algorithm Optimization

## Goal
Reduce execution time of the integer sorting function in `sort.py` when sorting an array of 1,000,000 random integers. The function must produce a correctly sorted output and preserve the caller's input list.

## Success Metric
- **Metric:** Execution time in seconds (median of 3 runs on 1M random integers, range 0--10,000,000)
- **Target:** < 0.5s
- **Direction:** minimize

## Constraints
- **Max iterations:** 20
- **Time budget per experiment:** 5 minutes
- **Pause for review every:** never
- **Evaluator:** `python benchmark.py`
- **Keep policy:** score_improvement
- **Guard:** `benchmark.py` correctness checks must pass and `sort_integers()` must return a correctly sorted copy without mutating the caller input
- **Noise runs:** 3
- **Min delta:** 0.001
- Pure Python only -- no C extensions, no Cython, no ctypes, no subprocess calls to compiled code
- Must handle edge cases: empty list, single element, already sorted, reverse sorted
- Function signature must remain: `def sort_integers(arr: list[int]) -> list[int]`
- No external libraries (only Python stdlib)

## Current Approach
Best approach: single-call `sorted()` which returns a new sorted list directly:

```python
def sort_integers(arr: list[int]) -> list[int]:
    return sorted(arr)
```

Why it won:
- Delegates the entire hot path to CPython's C-level Timsort
- `sorted()` internally creates the output list in one step (no separate copy needed)
- Zero Python-level overhead: no loops, no recursion, no intermediate allocations
- Marginally faster than `arr[:] + list.sort()` by avoiding the explicit copy step

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
| 0 | Baseline (rerun): recursive quicksort with list comprehensions | 2.117478s | -- | baseline | 2026-04-05 09:30 |
| 1 | Use CPython Timsort via `arr[:]` + `list.sort()` | 0.162183s | -92.3% | KEPT | 2026-04-05 09:31 |
| 2 | Use `sorted(arr)` single call to avoid explicit copy | 0.150459s | -92.9% | KEPT | 2026-04-05 09:32 |
| 3 | `list(arr)` + in-place sort vs `sorted()` | 0.156891s | -92.6% | REVERTED | 2026-04-05 09:33 |
| 4 | Counting sort with `array.array` -- Python loops over 10M range too slow | 0.653001s | -69.2% | REVERTED | 2026-04-05 09:34 |
| 5 | `array.array('l')` + `sorted()` -- conversion overhead kills benefit | 0.202860s | -90.4% | REVERTED | 2026-04-05 09:35 |
| 6 | `heapq.nsmallest(n, arr)` -- heapsort slower than Timsort | 0.175995s | -91.7% | REVERTED | 2026-04-05 09:36 |
| 7 | Chunk-sort + `heapq.merge` -- merge overhead exceeds cache benefit | 0.342458s | -83.8% | REVERTED | 2026-04-05 09:37 |
