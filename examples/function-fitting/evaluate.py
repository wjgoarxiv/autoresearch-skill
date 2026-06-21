#!/usr/bin/env python3
"""Mechanical evaluator for the function-fitting task."""

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
    except Exception:
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
    passed = rmse < 0.05

    print(json.dumps({"pass": passed, "score": score, "metric_value": round(rmse, 6)}))


if __name__ == "__main__":
    main()
