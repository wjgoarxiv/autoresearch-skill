# Final Report: Sorting Algorithm Optimization

## Executive Summary

Starting from a recursive quicksort baseline of **2.3991s** on 1M random integers, we achieved a final best of **0.1847s** -- a **92.3% reduction** in execution time over 11 iterations. The target of **< 0.5s** was first met at iteration 3 (0.4979s) using a micro-optimized LSD radix sort with base 65536.

The research explored two distinct performance regimes:
1. **Pure Python algorithms** (iterations 1-8): Best result 0.4226s (-82.4%) using `sorted()` as a stable sort subroutine in a 2-pass radix sort
2. **C-level stdlib** (iterations 9-10): Best result 0.1847s (-92.3%) using `list.sort()` in-place

## Best Result

| Metric | Value |
|--------|-------|
| **Algorithm** | `list.sort()` in-place (C Timsort) |
| **Median time** | 0.1847s |
| **vs Baseline** | -92.3% (from 2.3991s) |
| **Target** | < 0.5s -- MET (at iteration 3) |
| **Best pure Python** | 0.4486s (pre-computed dual histogram radix sort, iteration 6) |

## Iteration Summary

| # | Approach | Median | vs Best | Status |
|---|----------|--------|---------|--------|
| 0 | Baseline: recursive quicksort | 2.3991s | -- | baseline |
| 1 | Radix sort (LSD, base 256) | 0.8709s | -63.7% | KEPT |
| 2 | Radix sort (LSD, base 65536) | 0.5727s | -76.1% | KEPT |
| 3 | Micro-optimized radix (unrolled) | 0.4979s | -79.2% | KEPT -- TARGET MET |
| 4 | Counting sort (range 0-10M) | 0.6717s | +34.9% vs prev best | REVERTED |
| 5 | array module for count arrays | 0.6967s | +39.9% vs prev best | REVERTED |
| 6 | Pre-computed dual histograms | 0.4486s | -81.3% | KEPT |
| 7 | Radix base 2048 (11-bit, 3 passes) | 0.7205s | +60.6% vs prev best | REVERTED |
| 8 | sorted()-based radix (2 passes) | 0.4226s | -82.4% | KEPT |
| 9 | Direct sorted() (C Timsort) | 0.1920s | -92.0% | KEPT |
| 10 | list.sort() in-place | 0.1847s | -92.3% | KEPT |
| 11 | Hybrid bucket(256)+Timsort | 0.2494s | +35.0% vs prev best | REVERTED |

## Key Findings

### 1. Radix sort base matters enormously
- Base 256 (8-bit): 0.8709s (3 passes for 24-bit values)
- Base 65536 (16-bit): 0.5727s (2 passes)
- Base 2048 (11-bit): 0.7205s (3 passes)

Fewer passes always wins, even though larger base means larger count arrays. The scatter pass over 1M elements dominates the prefix sum over 65K elements.

### 2. Python per-element loop overhead is the bottleneck
Every Python-level `for x in arr` loop over 1M elements costs ~0.1-0.2s in pure interpreter overhead. This fundamentally limits pure Python sorting to ~0.4s minimum for 1M integers.

### 3. Pre-computing histograms in a single pass helps
Combining both radix histograms into one pass (iteration 6) saved ~10% over separate histogram passes. This reduced total passes from 4 (2 histogram + 2 scatter) to 3 (1 histogram + 2 scatter).

### 4. C-level sorted() is unbeatable for general-purpose sorting
`sorted()` and `list.sort()` use Timsort implemented in C, achieving ~0.18-0.19s. No pure Python approach can compete because the C implementation avoids per-element Python object overhead entirely.

### 5. Using sorted() as a radix subroutine is a clever middle ground
The 2-pass `sorted()` radix (iteration 8, 0.4226s) was faster than the best pure-Python radix (iteration 6, 0.4486s) because each `sorted()` call does its work in C. But it's slower than direct `sorted()` because the key function still requires Python-level evaluation.

## Failed Approaches

| Approach | Why It Failed |
|----------|---------------|
| **Counting sort (10M range)** | Allocating and iterating a 10M-element count array is expensive. Only efficient when range << n. |
| **array module for counts** | Python's `array` has slower per-element access than native lists due to boxing/unboxing overhead. |
| **Base 2048 radix (3 passes)** | The extra scatter pass over 1M elements costs more than the savings from smaller count arrays. |
| **Hybrid bucket+Timsort** | The Python-level distribution loop (1M iterations) adds ~0.07s overhead that eliminates any benefit from reduced comparison work in Timsort. |

## Conclusions

For integer sorting in pure Python:
- **LSD radix sort with base 65536** is optimal, achieving ~0.45s on 1M integers
- **Pre-computing histograms** in a single pass saves one full data scan
- **Unrolling the radix loop** into explicit passes avoids generic loop overhead

For production use:
- **`list.sort()`** (or `sorted()`) is always the right choice -- C Timsort is 2-4x faster than any pure Python algorithm
- The overhead of any Python-level per-element processing makes it impossible to compete with C-level sorting

## Output Files

- `sort.py` -- Final optimized implementation (list.sort() in-place)
- `research.md` -- Full research document with history table
- `research_log.md` -- Detailed log of each iteration's hypothesis, change, and result
- `autoresearch-results.tsv` -- Machine-readable results (12 rows, 8 columns)
- `results.png` / `results.pdf` -- Performance visualization (bar chart + convergence trajectory)
