# Research Report: Sorting Algorithm Optimization

**Generated:** 2026-03-15
**Total Iterations:** 8 (0-7, including baseline and reference)
**Final Metric:** 0.7513s median (minimize: execution time)
**Baseline:** 2.3991s
**Improvement:** -68.7%
**Status:** max_iterations_reached (target < 0.5s not achieved)

---

## Executive Summary

Starting from a naive recursive quicksort (2.40s), we explored 7 algorithmic variants to minimize sorting time on 1M random integers in pure Python. The key breakthrough came from abandoning comparison-based sorting entirely: LSD radix sort with base 65536 achieved 0.75s, a 68.7% improvement. One iteration (natural merge sort) was reverted after regressing on random data. The < 0.5s target was not reached — profiling suggests this is a fundamental CPython interpretation overhead ceiling for pure-Python sorting of 1M elements.

## Best Result

- **Iteration:** #6
- **Algorithm:** LSD Radix Sort, base 65536
- **Metric:** 0.7513s median (5 runs)
- **vs Baseline:** -1.6478s (-68.7%)
- **Complexity:** O(n * k) where k = 2 passes for 24-bit integers

```python
def sort_integers(arr):
    a = list(arr)
    if len(a) <= 1:
        return a
    min_val = min(a)
    if min_val < 0:
        a = [x - min_val for x in a]
    max_val = max(a)
    BITS, MASK = 16, 0xFFFF
    b = [0] * len(a)
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
```

## Iteration Summary

| # | Algorithm | Median | vs Baseline | vs Previous | Kept? |
|---|-----------|--------|-------------|-------------|-------|
| 0 | Recursive quicksort (baseline) | 2.3991s | -- | -- | -- |
| 1 | Bottom-up iterative merge sort | 1.8845s | -21.4% | -21.4% | Yes |
| 2 | Merge sort + insertion sort (32) | 1.7265s | -28.0% | -8.4% | Yes |
| 3 | Merge + binary insertion sort (64) | 1.6939s | -29.4% | -1.9% | Yes |
| 4 | Natural merge sort (Timsort-style) | 1.9504s | -18.7% | +15.1% | **No** |
| 5 | LSD radix sort, base 256 | 0.9817s | -59.1% | -42.1% | Yes |
| 6 | LSD radix sort, base 65536 | 0.7513s | -68.7% | -23.5% | Yes |
| 7 | Python sorted() [reference] | 0.1780s | -92.6% | -76.3% | Ref |

## Key Findings

1. **The comparison-sort ceiling is real.** Iterations 1-4 all used comparison-based sorting (merge sort variants). The best comparison-based result was 1.6939s — a 29.4% improvement through implementation tricks (iterative structure, insertion sort for small arrays, binary search). But no comparison-based pure-Python sort broke 1.5s.

2. **Radix sort is the paradigm shift.** Switching from O(n log n) comparison-based to O(n * k) radix sort produced a 42% jump in a single iteration (1.6939s -> 0.9817s). For integer data with bounded range, radix sort dominates.

3. **Base size matters more than expected.** Going from base 256 (3 passes) to base 65536 (2 passes) gave a 23.5% improvement. The memory cost (512KB counting array) is negligible compared to the data movement savings.

4. **Timsort's value is in its C implementation, not its algorithm.** Natural run detection (iteration 4) actually *regressed* on random data (+15.1%). The overhead of scanning for runs, reversing descending sequences, and maintaining run bookkeeping exceeded the savings. Python's built-in sorted() achieves 0.178s because Timsort is implemented in C, not because the algorithm is inherently faster.

5. **The CPython interpretation gap is ~4.2x.** Our best pure-Python sort (0.75s) is 4.2x slower than C-implemented sorted() (0.18s). This ratio is consistent with typical CPython interpretation overhead for tight numerical loops.

## Failed Approaches

1. **Natural merge sort (iteration 4):** Run detection overhead exceeded benefits on uniformly random data. Average natural run length in random data is ~2 elements — not enough to justify the bookkeeping cost.

2. **Target < 0.5s was not achievable** in pure Python. Extrapolating from the radix sort performance, achieving < 0.5s would require either: (a) C extensions, (b) numpy for vectorized operations, or (c) multiprocessing — all violating the pure-Python constraint.

## Recommendations

- **If the pure-Python constraint can be relaxed:** Use `sorted()` directly (0.178s) or numpy's `np.sort()` (likely ~0.05s). There's no practical reason to implement sorting in pure Python for production use.
- **If staying pure Python:** The base-65536 radix sort (0.75s) is the best option for integer data. For mixed-type data, the binary-insertion merge sort (v3, 1.69s) is the best comparison-based option.
- **Further exploration:** Could test radix sort with base 2^24 (single pass for 24-bit values) — but the 16M-entry counting array may cause cache pressure.

---

*Generated by the autoresearch-skill skill. See `research_log.md` for detailed iteration notes.*
