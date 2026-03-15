# Research Log: Sorting Algorithm Optimization

> Auto-generated on 2026-03-15
> Goal: Reduce execution time of sort_integers() on 1M random integers below 0.5s

---

## Iteration 0 — Baseline

**Hypothesis:** Establish baseline performance of recursive quicksort.

**Implementation:** Recursive quicksort with list comprehensions. Pivot = middle element. Three-way partition (left/middle/right).

**Measurement:**
```
Median: 2.3991s | Mean: 2.3882s | Stdev: 0.0599s
Runs:   [2.448, 2.4422, 2.3991, 2.3262, 2.3257]
```

**Analysis:** The baseline is 4.8x slower than the target. List comprehensions create three temporary lists per recursion level (O(n) copies). Recursion depth reaches O(log n) ~20 levels. Python function call overhead is significant at this scale.

**Decision:** Baseline established. Proceed with optimization.

---

## Iteration 1 — Bottom-up Iterative Merge Sort

**Hypothesis:** Eliminating recursion and using iterative bottom-up merge sort should reduce function call overhead and stack consumption.

**Changes:** Replaced recursive quicksort with iterative bottom-up merge sort. Pre-allocated output buffer `b = [0] * n`. Merges width-1 pairs, then width-2, then width-4, etc.

**Measurement:**
```
Median: 1.8845s | Mean: 1.8982s | Stdev: 0.0787s
Runs:   [2.0304, 1.8845, 1.8889, 1.8205, 1.867]
```

**Analysis:** 21.4% improvement. Removing recursion helped, but the merge operation still copies data between buffers. The improvement is moderate — the bottleneck is data movement, not call overhead.

**Decision:** KEPT. 2.3991s -> 1.8845s (-0.5146s)

---

## Iteration 2 — Merge Sort + Insertion Sort (RUN=32)

**Hypothesis:** Insertion sort is faster than merge sort for small arrays due to better cache locality and lower overhead. Using insertion sort for chunks < 32 should reduce the number of merge passes.

**Changes:** Added insertion sort pass for chunks of 32 elements before starting merge phase. Merge phase starts at width=32 instead of width=1.

**Measurement:**
```
Median: 1.7265s | Mean: 1.7596s | Stdev: 0.0824s
Runs:   [1.6862, 1.7265, 1.8181, 1.8732, 1.6937]
```

**Analysis:** Additional 8.4% improvement (cumulative 28.0%). Insertion sort's simplicity pays off for small subarrays — fewer comparisons, no buffer allocation, good cache behavior. The 32-element cutoff is a common sweet spot.

**Decision:** KEPT. 1.8845s -> 1.7265s (-0.1580s)

---

## Iteration 3 — Binary Insertion Sort (RUN=64)

**Hypothesis:** Binary search for the insertion point reduces comparisons from O(n) to O(log n) per element. Larger chunk size (64) should further reduce merge passes.

**Changes:** Replaced linear insertion sort with binary insertion sort. Increased chunk size from 32 to 64. Used list slice assignment for shifting.

**Measurement:**
```
Median: 1.6939s | Mean: 1.7249s | Stdev: 0.0943s
Runs:   [1.8493, 1.797, 1.6939, 1.653, 1.6314]
```

**Analysis:** Marginal improvement (1.9% over v2, cumulative 29.4%). Binary search reduces comparisons but list slice shifting is still O(n). Diminishing returns from comparison-based sort optimizations — the bottleneck is data movement in Python, not comparison count.

**Decision:** KEPT. 1.7265s -> 1.6939s (-0.0326s). Note: approaching diminishing returns for comparison-based approaches.

---

## Iteration 4 — Natural Merge Sort (Timsort-style)

**Hypothesis:** Detecting naturally occurring ascending/descending runs in the data should reduce work by avoiding unnecessary sorting of already-ordered subsequences. This is the key insight behind Python's Timsort.

**Changes:** Added run detection phase: scan for ascending runs and reversed descending runs. Extend short runs with insertion sort (MIN_RUN=32). Merge detected runs bottom-up.

**Measurement:**
```
Median: 1.9504s | Mean: 1.9551s | Stdev: 0.0437s
Runs:   [2.0182, 1.969, 1.9392, 1.9504, 1.8987]
```

**Analysis:** REGRESSION. 15.1% slower than v3, only 18.7% better than baseline. The run detection overhead (scanning, reversing descending runs, bookkeeping) costs more than it saves on random data. Random data has very few natural runs — average run length ~2. Timsort's run detection is valuable for real-world data that often has existing order, but harmful on uniformly random input. The C implementation of Timsort in CPython avoids this overhead through tight loops.

**Decision:** REVERTED. Run detection overhead exceeds benefit on random data. Stay with v3 (1.6939s).

**Key insight:** Timsort's genius is in its C implementation, not just its algorithm. The same algorithm in pure Python loses to simpler approaches due to interpretation overhead.

---

## Iteration 5 — LSD Radix Sort (Base 256)

**Hypothesis:** Comparison-based sorts are bounded by O(n log n). For integer sorting, radix sort achieves O(n * k) where k = number of digits. With base 256 and max value 10M (~24 bits), k = 3 passes. This should be dramatically faster.

**Changes:** Implemented LSD (Least Significant Digit) radix sort with base 256. Three passes through the data, each using counting sort on 8-bit digits. Handles negative numbers via offset.

**Measurement:**
```
Median: 0.9817s | Mean: 0.9611s | Stdev: 0.0932s
Runs:   [0.8935, 0.8451, 0.9817, 1.0041, 1.0813]
```

**Analysis:** Massive improvement — 59.1% faster than baseline, 42.1% faster than best comparison-based (v3). Breaking the O(n log n) barrier pays off enormously. Three linear passes beat 20 levels of merge operations. The counting sort inner loop is simple enough to be efficient even in Python.

**Decision:** KEPT. 1.6939s -> 0.9817s (-0.7122s). Paradigm shift from comparison-based to integer-specific sorting.

---

## Iteration 6 — LSD Radix Sort (Base 65536)

**Hypothesis:** Increasing the radix base from 256 to 65536 reduces the number of passes from 3 to 2 (for 24-bit values). Each pass is heavier (64K buckets vs 256) but eliminating a full data pass should net improve performance.

**Changes:** Changed BITS from 8 to 16, MASK from 0xFF to 0xFFFF. Counting array grows from 258 to 65538 entries. Now requires only 2 passes for values up to ~10M.

**Measurement:**
```
Median: 0.7513s | Mean: 0.7018s | Stdev: 0.077s
Runs:   [0.756, 0.7553, 0.7513, 0.5838, 0.6627]
```

**Analysis:** 23.5% improvement over base-256 radix sort, cumulative 68.7% vs baseline. Reducing from 3 passes to 2 is worth the larger counting array. Memory for 65K integers (~512KB) fits comfortably in L2 cache. This is the best achievable in pure Python without resorting to built-in sorted().

**Decision:** KEPT (BEST). 0.9817s -> 0.7513s (-0.2304s).

---

## Iteration 7 — Python Built-in sorted() [Reference]

**Hypothesis:** Python's sorted() uses Timsort implemented in C. This represents the practical performance ceiling for sorting in Python.

**Implementation:** `return sorted(arr)` — one line.

**Measurement:**
```
Median: 0.1780s | Mean: 0.178s | Stdev: 0.0091s
Runs:   [0.1703, 0.1707, 0.1928, 0.178, 0.1784]
```

**Analysis:** 92.6% faster than baseline, 76.3% faster than our best pure-Python implementation. The C implementation of Timsort is ~4.2x faster than our best pure-Python radix sort. This gap represents the fundamental interpretation overhead of CPython — no pure-Python algorithm can close it.

**Decision:** REFERENCE ONLY. Using sorted() is technically allowed but defeats the research goal of understanding algorithmic choices.

---

## Research Concluded

**Final best (pure Python):** 0.7513s (LSD radix sort, base 65536) — 68.7% improvement over baseline.

**Target status:** NOT REACHED. Target was < 0.5s; best achieved 0.7513s. The 0.5s target appears unreachable in pure Python for 1M integers without C extensions.

**Next steps:** See `final_report.md`.
