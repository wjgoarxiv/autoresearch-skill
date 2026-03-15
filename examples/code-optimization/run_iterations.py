"""
Auto-research loop runner: tests all sorting algorithm iterations sequentially.
Each iteration is a hypothesis -> experiment -> evaluate cycle.
"""

import json
import random
import statistics
import sys
import time

sys.setrecursionlimit(10_000)


def generate_test_data(n: int = 1_000_000, seed: int = 42) -> list[int]:
    rng = random.Random(seed)
    return [rng.randint(0, 10_000_000) for _ in range(n)]


def verify(sort_fn, label: str) -> bool:
    cases = [[], [1], [3, 1, 2], [5, 5, 5], list(range(100)), list(range(100, 0, -1))]
    for case in cases:
        if sort_fn(case[:]) != sorted(case):
            print(f"  [{label}] FAIL on {case[:10]}")
            return False
    return True


def bench(sort_fn, data: list[int], runs: int = 5) -> dict:
    times = []
    for i in range(runs):
        arr = data[:]
        t0 = time.perf_counter()
        result = sort_fn(arr)
        t1 = time.perf_counter()
        times.append(t1 - t0)
        if i == 0 and result != sorted(data):
            return {"error": "incorrect output", "median": 999}
    return {
        "median": round(statistics.median(times), 4),
        "mean": round(statistics.mean(times), 4),
        "min": round(min(times), 4),
        "max": round(max(times), 4),
        "stdev": round(statistics.stdev(times), 4) if len(times) > 1 else 0,
        "times": [round(t, 4) for t in times],
    }


# ── Iteration 0: Baseline (recursive quicksort) ─────────────────────────────
def sort_v0(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return sort_v0(left) + middle + sort_v0(right)


# ── Iteration 1: Bottom-up merge sort (avoid recursion overhead) ─────────────
def sort_v1(arr):
    a = list(arr)
    n = len(a)
    if n <= 1:
        return a
    b = [0] * n
    width = 1
    while width < n:
        for i in range(0, n, 2 * width):
            left = i
            mid = min(i + width, n)
            right = min(i + 2 * width, n)
            l, r, k = left, mid, left
            while l < mid and r < right:
                if a[l] <= a[r]:
                    b[k] = a[l]; l += 1
                else:
                    b[k] = a[r]; r += 1
                k += 1
            while l < mid:
                b[k] = a[l]; l += 1; k += 1
            while r < right:
                b[k] = a[r]; r += 1; k += 1
        a, b = b, a
        width *= 2
    return a


# ── Iteration 2: Merge sort + insertion sort for small subarrays ─────────────
def sort_v2(arr):
    a = list(arr)
    n = len(a)
    if n <= 1:
        return a

    # Insertion sort for small chunks first
    RUN = 32
    for start in range(0, n, RUN):
        end = min(start + RUN, n)
        for i in range(start + 1, end):
            key = a[i]
            j = i - 1
            while j >= start and a[j] > key:
                a[j + 1] = a[j]
                j -= 1
            a[j + 1] = key

    b = [0] * n
    width = RUN
    while width < n:
        for i in range(0, n, 2 * width):
            left = i
            mid = min(i + width, n)
            right = min(i + 2 * width, n)
            l, r, k = left, mid, left
            while l < mid and r < right:
                if a[l] <= a[r]:
                    b[k] = a[l]; l += 1
                else:
                    b[k] = a[r]; r += 1
                k += 1
            while l < mid:
                b[k] = a[l]; l += 1; k += 1
            while r < right:
                b[k] = a[r]; r += 1; k += 1
        a, b = b, a
        width *= 2
    return a


# ── Iteration 3: Merge sort + binary insertion sort (faster comparisons) ─────
def sort_v3(arr):
    import bisect
    a = list(arr)
    n = len(a)
    if n <= 1:
        return a

    RUN = 64  # Larger chunks with binary insertion sort
    for start in range(0, n, RUN):
        end = min(start + RUN, n)
        for i in range(start + 1, end):
            key = a[i]
            # Binary search for insertion point within [start, i)
            lo, hi = start, i
            while lo < hi:
                mid = (lo + hi) // 2
                if a[mid] <= key:
                    lo = mid + 1
                else:
                    hi = mid
            # Shift elements right
            a[lo + 1:i + 1] = a[lo:i]
            a[lo] = key

    b = [0] * n
    width = RUN
    while width < n:
        for i in range(0, n, 2 * width):
            left = i
            mid_idx = min(i + width, n)
            right = min(i + 2 * width, n)
            l, r, k = left, mid_idx, left
            while l < mid_idx and r < right:
                if a[l] <= a[r]:
                    b[k] = a[l]; l += 1
                else:
                    b[k] = a[r]; r += 1
                k += 1
            while l < mid_idx:
                b[k] = a[l]; l += 1; k += 1
            while r < right:
                b[k] = a[r]; r += 1; k += 1
        a, b = b, a
        width *= 2
    return a


# ── Iteration 4: Natural merge sort (detect existing runs, Timsort-style) ────
def sort_v4(arr):
    a = list(arr)
    n = len(a)
    if n <= 1:
        return a

    MIN_RUN = 32

    def _insertion_sort(a, lo, hi):
        for i in range(lo + 1, hi):
            key = a[i]
            j = i - 1
            while j >= lo and a[j] > key:
                a[j + 1] = a[j]
                j -= 1
            a[j + 1] = key

    # Find natural runs and extend short ones with insertion sort
    runs = []
    i = 0
    while i < n:
        run_start = i
        if i + 1 < n:
            if a[i] <= a[i + 1]:
                # Ascending run
                while i + 1 < n and a[i] <= a[i + 1]:
                    i += 1
            else:
                # Descending run -> reverse it
                while i + 1 < n and a[i] > a[i + 1]:
                    i += 1
                a[run_start:i + 1] = a[run_start:i + 1][::-1]
        i += 1
        # Extend short runs with insertion sort
        if i - run_start < MIN_RUN:
            end = min(run_start + MIN_RUN, n)
            _insertion_sort(a, run_start, end)
            i = end
        runs.append((run_start, min(i, n)))

    # Merge runs bottom-up
    b = [0] * n
    while len(runs) > 1:
        new_runs = []
        for j in range(0, len(runs), 2):
            if j + 1 < len(runs):
                l_start, l_end = runs[j]
                r_start, r_end = runs[j + 1]
                l, r, k = l_start, r_start, l_start
                while l < l_end and r < r_end:
                    if a[l] <= a[r]:
                        b[k] = a[l]; l += 1
                    else:
                        b[k] = a[r]; r += 1
                    k += 1
                while l < l_end:
                    b[k] = a[l]; l += 1; k += 1
                while r < r_end:
                    b[k] = a[r]; r += 1; k += 1
                a[l_start:r_end] = b[l_start:r_end]
                new_runs.append((l_start, r_end))
            else:
                new_runs.append(runs[j])
        runs = new_runs

    return a


# ── Iteration 5: LSD Radix sort (integer-specific, O(n*k)) ──────────────────
def sort_v5(arr):
    a = list(arr)
    if len(a) <= 1:
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

    # LSD radix sort, base 256
    BITS = 8
    MASK = (1 << BITS) - 1
    b = [0] * len(a)

    shift = 0
    while (max_val >> shift) > 0:
        count = [0] * (MASK + 2)
        for x in a:
            digit = (x >> shift) & MASK
            count[digit + 1] += 1
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


# ── Iteration 6: Radix sort with larger base (base 65536) ───────────────────
def sort_v6(arr):
    a = list(arr)
    if len(a) <= 1:
        return a

    min_val = min(a)
    if min_val < 0:
        a = [x - min_val for x in a]

    max_val = max(a)
    if max_val == 0:
        if min_val < 0:
            return [x + min_val for x in a]
        return a

    BITS = 16
    MASK = (1 << BITS) - 1
    b = [0] * len(a)

    shift = 0
    while (max_val >> shift) > 0:
        count = [0] * (MASK + 2)
        for x in a:
            digit = (x >> shift) & MASK
            count[digit + 1] += 1
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


# ── Iteration 7: Python built-in sorted() (reference) ───────────────────────
def sort_v7(arr):
    return sorted(arr)


# ── Run all iterations ───────────────────────────────────────────────────────
ITERATIONS = [
    ("v0", "Baseline: recursive quicksort with list comprehensions", sort_v0),
    ("v1", "Bottom-up iterative merge sort (eliminate recursion)", sort_v1),
    ("v2", "Merge sort + insertion sort for subarrays < 32", sort_v2),
    ("v3", "Merge sort + binary insertion sort, chunk size 64", sort_v3),
    ("v4", "Natural merge sort with run detection (Timsort-style)", sort_v4),
    ("v5", "LSD radix sort, base 256", sort_v5),
    ("v6", "LSD radix sort, base 65536 (fewer passes)", sort_v6),
    ("v7", "Python built-in sorted() [reference]", sort_v7),
]


def main():
    data = generate_test_data()
    reference = sorted(data)
    results = []

    for tag, desc, fn in ITERATIONS:
        print(f"\n{'='*60}")
        print(f"Iteration {tag}: {desc}")
        print(f"{'='*60}")

        if not verify(fn, tag):
            print(f"  SKIPPED (correctness failure)")
            results.append({"tag": tag, "desc": desc, "error": "correctness failure"})
            continue

        r = bench(fn, data, runs=5)
        if "error" in r:
            print(f"  FAILED: {r['error']}")
            results.append({"tag": tag, "desc": desc, "error": r["error"]})
            continue

        print(f"  Median: {r['median']}s | Mean: {r['mean']}s | Stdev: {r['stdev']}s")
        print(f"  Runs:   {r['times']}")
        results.append({"tag": tag, "desc": desc, **r})

    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    baseline = results[0].get("median", 999)
    print(f"{'Tag':<5} {'Median':>8} {'vs Base':>10} {'Description'}")
    print(f"{'-'*5} {'-'*8} {'-'*10} {'-'*40}")
    for r in results:
        if "error" in r:
            print(f"{r['tag']:<5} {'ERROR':>8} {'':>10} {r['desc']}")
        else:
            delta = r["median"] - baseline
            pct = (delta / baseline) * 100 if baseline > 0 else 0
            print(f"{r['tag']:<5} {r['median']:>7.4f}s {pct:>+9.1f}% {r['desc']}")

    # JSON output
    print(f"\n__RESULTS_JSON__:{json.dumps(results)}")


if __name__ == "__main__":
    main()
