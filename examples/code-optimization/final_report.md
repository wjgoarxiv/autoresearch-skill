# Final Report: Sorting Algorithm Optimization

## Best Result

| Metric | Value |
|--------|-------|
| **Best median time** | 0.150459s (iteration 2) |
| **Confirmation run** | 0.158868s |
| **Baseline** | 2.117478s |
| **Improvement** | -92.9% from baseline |
| **Target (< 0.5s)** | ACHIEVED at iteration 1 |
| **Pass** | true |

## Winning Solution

```python
def sort_integers(arr: list[int]) -> list[int]:
    return sorted(arr)
```

A single call to Python's built-in `sorted()`, which delegates entirely to CPython's C-level Timsort implementation.

## Iteration Summary

| # | Approach | Median (s) | vs Best | Result |
|---|----------|-----------|---------|--------|
| 0 | Naive recursive quicksort (baseline) | 2.117 | -- | baseline |
| 1 | `arr[:] + list.sort()` (Timsort) | 0.162 | -- | KEPT |
| 2 | `sorted(arr)` single call | 0.150 | -7.2% | KEPT (best) |
| 3 | `list(arr) + list.sort()` | 0.157 | +4.3% | REVERTED |
| 4 | Counting sort with `array.array` | 0.653 | +334% | REVERTED |
| 5 | `array.array('l') + sorted()` | 0.203 | +34.8% | REVERTED |
| 6 | `heapq.nsmallest(n, arr)` | 0.176 | +17.0% | REVERTED |
| 7 | Chunk-sort + `heapq.merge` | 0.342 | +128% | REVERTED |

## Approaches Tried

### Category 1: Delegating to C-level built-ins (iterations 1-3)
- **`arr[:] + list.sort()`** -- Fast (0.162s). Copy + in-place sort.
- **`sorted(arr)`** -- Fastest (0.150s). Creates and returns sorted copy in one C call.
- **`list(arr) + list.sort()`** -- Slightly slower (0.157s). `list()` constructor marginally slower than slice copy.

**Conclusion:** `sorted()` is the optimal single-call approach. It avoids the separate copy step that `arr[:] + sort()` requires.

### Category 2: Alternative data structures (iterations 4-5)
- **Counting sort with `array.array`** -- O(n+k) theoretically, but Python-level loops over the 10M-element count array are catastrophically slow (0.653s).
- **`array.array('l') + sorted()`** -- Converting list to contiguous C memory then sorting. The conversion overhead (0.203s) outweighs any iteration speedup.

**Conclusion:** Any approach that adds Python-level loops or data conversion before the C sort loses badly. The bottleneck is Python interpreter overhead, not algorithmic complexity.

### Category 3: Alternative sorting algorithms (iteration 6)
- **`heapq.nsmallest(n, arr)`** -- C-level heapsort. Slower (0.176s) due to worse cache locality than Timsort's merge-based approach.

**Conclusion:** Timsort's adaptive merge sort beats heapsort even when both run in C.

### Category 4: Divide-and-conquer with merge (iteration 7)
- **Chunk-sort + `heapq.merge`** -- Sort 250K-element chunks, merge with C-level `heapq.merge`. Much slower (0.342s) due to Python overhead of slicing, list creation, and `list()` conversion of the merge iterator.

**Conclusion:** Splitting work into chunks adds enough Python-level overhead to negate any cache benefit. Timsort already handles cache efficiency internally.

## Key Insights

1. **CPython's Timsort is nearly unbeatable in pure Python.** It runs entirely in C, is highly optimized for real-world data, and any Python-level wrapper adds measurable overhead.

2. **`sorted()` > `arr[:] + list.sort()`.** The single-call `sorted()` is marginally faster because it avoids a separate copy step. `sorted()` allocates and fills the output list during the sort itself.

3. **Python-level loops are the bottleneck.** Any algorithm that requires Python `for` loops over large arrays (counting sort, radix sort) cannot compete with C-level sorting, even if the algorithm has better asymptotic complexity.

4. **Data conversion is expensive.** Converting between list and `array.array` adds enough overhead to negate any benefit from contiguous memory layout.

5. **The optimal pure-Python sort is a one-liner.** No amount of algorithmic cleverness in pure Python can beat delegating to the C runtime.

## Recommendations

- **Use `sorted(arr)` for production code.** It is the fastest, simplest, and most readable solution.
- **For further optimization beyond pure Python:** Use NumPy's `np.sort()` (forbidden by constraints) or Cython/C extensions.
- **Timsort's adaptiveness is a feature:** For partially sorted data, it performs even better than the random-input benchmark suggests.
