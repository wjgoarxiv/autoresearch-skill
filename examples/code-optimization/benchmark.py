"""Benchmark harness for sort_integers(). Emits only evaluator-contract JSON."""

import importlib
import json
import random
import statistics
import sys
import time


def generate_test_data(n: int = 1_000_000, seed: int = 42) -> list[int]:
    rng = random.Random(seed)
    return [rng.randint(0, 10_000_000) for _ in range(n)]


def verify_correctness(sort_fn) -> bool:
    """Verify sort correctness on edge cases."""
    cases = [
        [],
        [1],
        [3, 1, 2],
        [5, 5, 5],
        list(range(100)),          # already sorted
        list(range(100, 0, -1)),   # reverse sorted
    ]
    for case in cases:
        result = sort_fn(case[:])
        if result != sorted(case):
            print(f"FAIL: input={case[:20]}... expected={sorted(case)[:20]}... got={result[:20]}...")
            return False

    # Stability check: sort by value, equal elements should keep original order
    # We test with a list that has duplicate values
    data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    result = sort_fn(data[:])
    if result != sorted(data):
        print(f"FAIL: stability/correctness check failed")
        return False

    return True


def benchmark(sort_fn, data: list[int], runs: int = 3) -> dict:
    """Run sort_fn on data for N runs. Return timing stats."""
    times = []
    for i in range(runs):
        arr = data[:]  # fresh copy each run
        t0 = time.perf_counter()
        result = sort_fn(arr)
        t1 = time.perf_counter()
        times.append(t1 - t0)
        # Verify output on first run
        if i == 0 and result != sorted(data):
            return {"error": "incorrect output", "times": times}

    return {
        "median": round(statistics.median(times), 6),
        "mean": round(statistics.mean(times), 6),
        "min": round(min(times), 6),
        "max": round(max(times), 6),
        "stdev": round(statistics.stdev(times), 6) if len(times) > 1 else 0,
        "times": [round(t, 4) for t in times],
    }


def main():
    # Increase recursion limit for baseline quicksort
    sys.setrecursionlimit(10_000)

    # Import the sort function
    import sort
    importlib.reload(sort)

    if not verify_correctness(sort.sort_integers):
        print(json.dumps({"pass": False, "score": -999.0}))
        sys.exit(1)
    data = generate_test_data()
    results = benchmark(sort.sort_integers, data, runs=3)

    if "error" in results:
        print(json.dumps({"pass": False, "score": -999.0}))
        sys.exit(1)
    evaluator = {"pass": bool(results["median"] < 0.5), "score": -results["median"]}
    print(json.dumps(evaluator))


if __name__ == "__main__":
    main()
