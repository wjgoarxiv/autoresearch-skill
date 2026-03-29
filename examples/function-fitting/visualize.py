#!/usr/bin/env python3
"""Visualize the prediction vs actual data."""

import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def load_csv(path):
    with open(path) as f:
        reader = csv.DictReader(f)
        return [(float(r["x"]), float(r["y"])) for r in reader]


def main():
    from predict import predict

    train = load_csv("train_data.csv")
    test = load_csv("test_data.csv")

    xs = np.linspace(-3, 3, 500)
    ys_pred = [predict(x) for x in xs]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter([p[0] for p in train], [p[1] for p in train],
               alpha=0.4, s=20, label="Train data", color="#2196F3")
    ax.scatter([p[0] for p in test], [p[1] for p in test],
               alpha=0.6, s=30, label="Test data", color="#FF9800", marker="x")
    ax.plot(xs, ys_pred, color="#E91E63", linewidth=2, label="Prediction")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Function Fitting: Prediction vs Data")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("results.png", dpi=150)
    print("Saved results.png")


if __name__ == "__main__":
    main()
