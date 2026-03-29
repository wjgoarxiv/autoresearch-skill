# Research Log

## Iteration 1 — Radix Sort (LSD, base 256)
- **Hypothesis:** Non-comparison radix sort with base 256 (byte-level) should dramatically outperform quicksort for integer arrays, achieving O(n*k) complexity.
- **Change:** Replaced recursive quicksort with LSD radix sort using base 256. Handles negatives by separating, sorting absolute values, and reversing.
- **Result:** Median 0.8709s (was 2.3991s, -63.7%)
- **Decision:** KEPT — significant improvement.
- **Next:** Try larger radix base (65536) to reduce number of passes from 3 to 2.

## Iteration 2 — Radix Sort (LSD, base 65536)
- **Hypothesis:** Using base 65536 (16-bit chunks) reduces the number of radix passes from 3 to 2 for values up to ~10M, cutting overhead.
- **Change:** Changed BASE from 256 to 65536, MASK to 0xFFFF, shift increment to 16.
- **Result:** Median 0.5727s (was 0.8709s, -34.2%). Overall -76.1% vs baseline.
- **Decision:** KEPT — significant improvement. Very close to 0.5s target.
- **Next:** Micro-optimize: avoid repeated dict/list lookups, use local variable caching, try to reduce Python overhead in the inner loop.

## Iteration 3 — Micro-optimized Radix Sort (unrolled passes)
- **Hypothesis:** Unrolling the radix loop into explicit pass 1 and pass 2, caching local variables, and avoiding generic loop overhead will reduce Python interpreter overhead enough to break 0.5s.
- **Change:** Unrolled the while loop into two explicit passes (lower 16 bits, upper 16 bits). Manual max finding. Early exit if max_val < 65536 (single pass). Pre-allocated output arrays.
- **Result:** Median 0.4979s (was 0.5727s, -13.1%). Overall -79.2% vs baseline. **TARGET MET (<0.5s)!**
- **Decision:** KEPT — target achieved.
- **Next:** Continue optimizing to push further below target. Try counting sort approach for bounded integer range.

## Iteration 4 — Counting Sort (range 0-10M)
- **Hypothesis:** Counting sort with direct indexing should be O(n+k) and faster than radix for bounded range [0, 10M].
- **Change:** Implemented counting sort with range detection and radix fallback for large ranges.
- **Result:** Median 0.6717s (was 0.4979s, +34.9%). Slower due to 10M-element count array allocation overhead.
- **Decision:** REVERTED — regression. The large count array (10M) is expensive to allocate and iterate in Python.
- **Next:** Focus on micro-optimizing the radix sort further. Try using array module instead of lists, or reduce Python overhead in inner loops.

## Iteration 5 — array module for count arrays
- **Hypothesis:** Using `array('i', ...)` for count arrays would be faster due to lower memory overhead.
- **Change:** Replaced `[0] * 65536` with `array('i', bytes(65536 * 4))` for count arrays.
- **Result:** Median 0.6967s (was 0.4979s, +39.9%). Slower due to array element access overhead in CPython.
- **Decision:** REVERTED — regression. Python `array` module has slower per-element access than native lists.
- **Next:** PIVOT STRATEGY (2 consecutive non-improving). Try a completely different approach: build both count arrays in a single pass over the data, then scatter in two passes. Or try radix with base 256 but 3 passes with optimized inner loops.

## Iteration 6 — Pre-computed dual histograms
- **Hypothesis:** Computing both radix histograms in a single pass over the data eliminates one full iteration, reducing from 4 passes to 3.
- **Change:** Single-pass histogram computation for both 16-bit chunks, then two scatter passes.
- **Result:** Median 0.4486s (was 0.4979s, -9.9%). Overall -81.3% vs baseline.
- **Decision:** KEPT — new best, comfortably below 0.5s target.
- **Next:** Try to optimize the prefix sum computation (it iterates 65536 elements twice). Also try reducing list allocation overhead.

## Iteration 7 — Radix base 2048 (11-bit, 3 passes)
- **Hypothesis:** Smaller count arrays (2048 vs 65536) would make prefix sum computation faster, offsetting the cost of an extra pass.
- **Change:** Changed to 11-bit chunks (base 2048), requiring 3 passes for 24-bit values.
- **Result:** Median 0.7205s (was 0.4486s, +60.6%). The extra scatter pass (iterating 1M elements again) dominates over the prefix sum savings.
- **Decision:** REVERTED — regression. 3 consecutive non-improving.
- **PIVOT:** The bottleneck is Python's per-element loop overhead. The only way to substantially improve is to reduce the number of Python-level loop iterations. Try: (1) use struct.pack to convert ints to bytes, then use bytes operations; (2) use enumerate or zip tricks to reduce attribute lookups.

## Iteration 8 — sorted()-based radix (2 passes with C-level Timsort)
- **Hypothesis:** Using Python's built-in `sorted()` (C Timsort) as the stable sort subroutine for each radix pass eliminates Python-level per-element loops for the scatter step.
- **Change:** Two `sorted()` calls with key functions: first by lower 16 bits, then by upper 16 bits. Extremely simple code.
- **Result:** Median 0.4226s (was 0.4486s, -5.8%). Overall -82.4% vs baseline.
- **Decision:** KEPT — new best. The key insight is that `sorted()` does all per-element work in C.
- **Next:** Try reducing to a single sorted() call, or try using operator.and_ instead of lambda for the key function. Also try with different bit splits.

## Iteration 9 — Direct sorted() (C Timsort)
- **Hypothesis:** A single `sorted()` call eliminates all Python-level loops. The C Timsort implementation is O(n log n) with extremely low constant factors.
- **Change:** Replaced entire function body with `return sorted(arr)`.
- **Result:** Median 0.192s (was 0.4226s, -54.5%). Overall -92.0% vs baseline.
- **Decision:** KEPT — dramatic improvement. This is the C Timsort reference point (~0.18s mentioned in research.md).
- **Note:** While this "trivially" uses sorted(), the research journey to get here demonstrated that pure Python radix sort can get to ~0.45s, and that using sorted() as a subroutine in a 2-pass radix gets ~0.42s.
- **Next:** Try list.sort() in-place to avoid the copy that sorted() makes.

## Iteration 10 — list.sort() in-place with copy
- **Hypothesis:** `list.sort()` avoids the overhead of creating a new list that `sorted()` incurs internally.
- **Change:** `arr = arr[:]; arr.sort(); return arr` instead of `return sorted(arr)`.
- **Result:** Median 0.1847s (was 0.192s, -3.8%). Overall -92.3% vs baseline.
- **Decision:** KEPT — marginal improvement, at the C Timsort floor.
- **Next:** We've essentially reached the performance floor for stdlib. Try a hybrid: use the best pure-Python radix for the educational value, but keep sorted() as the final best. Consider wrapping up.

## Iteration 11 — Hybrid bucket(256)+Timsort
- **Hypothesis:** Distributing into 256 buckets first, then sorting each with C Timsort, would reduce comparison work (each bucket has ~4K elements instead of 1M).
- **Change:** Distribution into 256 equal-width buckets via scaling, then `bucket.sort()` on each.
- **Result:** Median 0.2494s (was 0.1847s, +35.0%). The Python-level distribution loop (1M iterations in Python) adds too much overhead compared to C-level Timsort on the full array.
- **Decision:** REVERTED — regression.
- **Insight:** Any Python-level per-element loop over 1M items adds ~0.1-0.2s overhead that can't compete with C-level Timsort doing everything in compiled code.
