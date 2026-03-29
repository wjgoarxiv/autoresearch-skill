#!/usr/bin/env python3
"""Generate training and test data from a hidden composite function.

The hidden function combines polynomial, trigonometric, and exponential components
to create a curve that is non-trivial to discover but deterministic.

Hidden function:
    y = 0.5*sin(3x) + 0.3*cos(7x) + 0.08*x^2 - 0.15*x + 0.2*exp(-0.5*x^2) + noise

This requires the agent to discover:
1. Multiple sinusoidal frequencies (3, 7)
2. A polynomial component (quadratic + linear)
3. A Gaussian bump (exp term)
4. The correct coefficients for each

Output: train_data.csv (80 points), test_data.csv (40 points)
"""

import csv
import math
import random

SEED = 42
NOISE_STD = 0.03
X_MIN, X_MAX = -3.0, 3.0
N_TRAIN = 80
N_TEST = 40


def hidden_function(x: float) -> float:
    return (
        0.5 * math.sin(3 * x)
        + 0.3 * math.cos(7 * x)
        + 0.08 * x ** 2
        - 0.15 * x
        + 0.2 * math.exp(-0.5 * x ** 2)
    )


def generate_points(n: int, rng: random.Random) -> list[tuple[float, float]]:
    points = []
    for _ in range(n):
        x = rng.uniform(X_MIN, X_MAX)
        y = hidden_function(x) + rng.gauss(0, NOISE_STD)
        points.append((round(x, 6), round(y, 6)))
    return sorted(points, key=lambda p: p[0])


def write_csv(path: str, points: list[tuple[float, float]]) -> None:
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["x", "y"])
        for x, y in points:
            writer.writerow([x, y])


def main() -> None:
    rng = random.Random(SEED)
    train = generate_points(N_TRAIN, rng)
    test = generate_points(N_TEST, rng)
    write_csv("train_data.csv", train)
    write_csv("test_data.csv", test)
    print(f"Generated {N_TRAIN} training points -> train_data.csv")
    print(f"Generated {N_TEST} test points -> test_data.csv")


if __name__ == "__main__":
    main()
