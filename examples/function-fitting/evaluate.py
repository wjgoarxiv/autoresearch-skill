#!/usr/bin/env python3
"""Mechanical evaluator for the function-fitting task.

Reads test_data.csv, runs predict(x) for each point, computes RMSE.
Outputs JSON: {"pass": bool, "score": float}

- pass: true if RMSE < 0.50 (generous bar — baseline is ~0.7)
- score: negative RMSE (higher is better, for score_improvement policy)

Usage: python evaluate.py
"""

import csv
import json
import math
import sys


def main() -> None:
    # Import the predict function
    try:
        from predict import predict
    except ImportError:
        print(json.dumps({"pass": False, "score": -99.0}))
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"pass": False, "score": -99.0}))
        sys.exit(0)

    # Load test data
    try:
        with open("test_data.csv") as f:
            reader = csv.DictReader(f)
            points = [(float(row["x"]), float(row["y"])) for row in reader]
    except FileNotFoundError:
        print(json.dumps({"pass": False, "score": -99.0}))
        sys.exit(0)

    if not points:
        print(json.dumps({"pass": False, "score": -99.0}))
        sys.exit(0)

    # Compute RMSE
    squared_errors = []
    for x, y_true in points:
        try:
            y_pred = predict(x)
            squared_errors.append((y_true - y_pred) ** 2)
        except Exception:
            squared_errors.append(100.0)  # penalty for crashes

    rmse = math.sqrt(sum(squared_errors) / len(squared_errors))

    # Score is negative RMSE (higher = better) for score_improvement policy
    score = round(-rmse, 6)
    passed = rmse < 0.50

    print(json.dumps({"pass": passed, "score": score}))


if __name__ == "__main__":
    main()
