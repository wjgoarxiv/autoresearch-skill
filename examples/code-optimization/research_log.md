# Research Log: Sorting Algorithm Optimization

## Iteration 0 — Baseline
- **Approach:** Naive recursive quicksort with list comprehensions
- **Median time:** 2.117478s
- **Pass:** false
- **Notes:** Python-level recursion, 3 list comprehensions per partition, heavy object allocation. Far from 0.5s target.

## Iteration 7 — Chunk-sort + heapq.merge
- **Hypothesis:** Split array into 250K-element chunks, sort each with `sorted()` for cache locality, merge with C-level `heapq.merge()`.
- **Median time:** 0.342458s
- **Delta vs prev best:** +0.191999s (+127.6%)
- **Pass:** true
- **Status:** REVERTED
- **Notes:** The Python overhead of slicing into chunks, creating chunk lists, and `list(_merge(*chunks))` conversion far exceeds any cache benefit. `sorted()` on the full array is already cache-efficient in its C implementation.

## Iteration 6 — heapq.nsmallest (PIVOT attempt)
- **Hypothesis:** `heapq.nsmallest(n, arr)` uses C-level heap operations and returns a new sorted list. For n=len(arr) it's effectively a heapsort.
- **Median time:** 0.175995s
- **Delta vs prev best:** +0.025536s (+17.0%)
- **Pass:** true
- **Status:** REVERTED
- **Notes:** Heapsort has worse cache locality than Timsort's merge-based approach. O(n log n) in both cases, but constant factors favor Timsort.

## Iteration 5 — array.array + sorted() (PIVOT TRIGGER)
- **Hypothesis:** Packing ints into `array.array('l')` for contiguous C memory, then calling `sorted()`, might benefit from faster iteration over C-contiguous data.
- **Median time:** 0.202860s
- **Delta vs prev best:** +0.052401s (+34.8%)
- **Pass:** true
- **Status:** REVERTED
- **Notes:** The cost of converting list -> array.array outweighs any iteration speedup. 3 consecutive non-improving iterations -- PIVOT required. 
- **PIVOT:** All pure-Python alternatives to `sorted()` are slower. The C-level Timsort is nearly unbeatable. New strategy: focus on reducing the *input* work -- pre-processing or partitioning that lets Timsort work on already-partially-sorted data, or reducing Python-level overhead around the `sorted()` call.

## Iteration 4 — Counting sort with array.array
- **Hypothesis:** Counting sort is O(n+k) for integers in bounded range [0, 10M]. Using `array.array('I')` for contiguous count storage should be cache-friendly.
- **Median time:** 0.653001s
- **Delta vs prev best:** +0.502542s (+334.0%)
- **Pass:** false
- **Status:** REVERTED
- **Notes:** Pure Python loops over 10M range are catastrophically slow. The Python `for` loop and index operations on `array.array` can't compete with C-level Timsort. Counting sort only wins when the counting/output loops run in C.

## Iteration 3 — list(arr) + in-place sort
- **Hypothesis:** `list(arr)` constructor copy + `out.sort()` may reduce allocation overhead vs `sorted()`.
- **Median time:** 0.156891s
- **Delta vs prev best:** +0.006432s (+4.3%)
- **Pass:** true
- **Status:** REVERTED
- **Notes:** Slightly slower than `sorted()`. The `list()` constructor + separate `.sort()` adds overhead vs single `sorted()` call.

## Iteration 2 — sorted() single call
- **Hypothesis:** `sorted(arr)` avoids the explicit `arr[:]` copy since it creates a new list internally, reducing one allocation.
- **Median time:** 0.150459s
- **Delta vs prev best:** -0.011724s (-7.2%)
- **Pass:** true
- **Status:** KEPT
- **Notes:** Small but real improvement. `sorted()` slightly more efficient than copy + in-place sort.

## Iteration 1 — list.sort() Timsort
- **Hypothesis:** Replacing recursive quicksort with `arr[:] + list.sort()` (CPython C-level Timsort) eliminates Python-level recursion and partition overhead.
- **Median time:** 0.162183s
- **Delta:** -1.955295s (-92.3%)
- **Pass:** true
- **Status:** KEPT
- **Notes:** Huge speedup. Target achieved (< 0.5s). Exploring further optimizations.

---
