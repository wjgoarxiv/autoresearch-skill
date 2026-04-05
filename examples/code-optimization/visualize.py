#!/usr/bin/env python3
"""Generate a TSV-driven visualization for the sorting optimization example."""

import csv
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))
from style_presets import rcparams

rcparams()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET = 0.5
COL_KEPT = "#0072B2"
COL_REVERTED = "#D55E00"
COL_BEST = "#009E73"
COL_TARGET = "#E69F00"
COL_OTHER = "#999999"


def load_rows() -> list[dict]:
    path = os.path.join(SCRIPT_DIR, "autoresearch-results.tsv")
    with open(path) as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def parse_rows(rows: list[dict]) -> list[dict]:
    parsed = []
    best_metric = None
    for row in rows:
        metric = float(row["metric_value"])
        status = row["status"].strip()
        if best_metric is None:
            best_metric = metric
        elif status == "improved":
            best_metric = min(best_metric, metric)
        parsed.append(
            {
                "iteration": int(row["iteration"]),
                "metric": metric,
                "status": status,
                "description": row["description"].strip(),
                "best": best_metric,
            }
        )
    return parsed


def main() -> None:
    rows = parse_rows(load_rows())
    xs = [row["iteration"] for row in rows]
    metrics = [row["metric"] for row in rows]
    bests = [row["best"] for row in rows]
    labels = [f"Iter {x}" for x in xs]
    colors = []
    for row in rows:
        if row["status"] in ("baseline", "improved"):
            colors.append(COL_KEPT)
        elif row["status"] == "reverted":
            colors.append(COL_REVERTED)
        else:
            colors.append(COL_OTHER)

    fig, (ax1, ax2) = plt.subplots(
        2,
        1,
        figsize=(11, 8),
        gridspec_kw={"height_ratios": [3, 2], "hspace": 0.4},
    )

    ax1.text(-0.08, 1.05, "A", transform=ax1.transAxes, fontsize=16, fontweight="bold", va="top")
    ax2.text(-0.08, 1.05, "B", transform=ax2.transAxes, fontsize=16, fontweight="bold", va="top")

    bars = ax1.bar(xs, metrics, color=colors, width=0.6, edgecolor="white", linewidth=0.8)
    ax1.axhline(TARGET, color=COL_TARGET, linestyle="--", linewidth=1.5)
    for bar, row in zip(bars, rows):
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.03,
            f"{row['metric']:.3f}s",
            ha="center",
            va="bottom",
            fontsize=9,
        )
    ax1.set_ylabel("Median runtime (s)")
    ax1.set_xticks(xs)
    ax1.set_xticklabels(labels)
    ax1.set_title("Sorting Optimization Rerun (v2.0 Controls)")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.legend(
        handles=[
            Patch(facecolor=COL_KEPT, label="Baseline / kept"),
            Patch(facecolor=COL_REVERTED, label="Reverted"),
            Line2D([0], [0], color=COL_TARGET, linestyle="--", linewidth=1.5, label="Target < 0.5s"),
        ],
        loc="upper right",
        frameon=True,
        edgecolor="black",
    )

    ax2.plot(xs, metrics, color=COL_OTHER, marker="o", linewidth=1.2, label="Each iteration")
    ax2.plot(xs, bests, color=COL_BEST, marker="o", linewidth=2.5, label="Best so far")
    ax2.axhline(TARGET, color=COL_TARGET, linestyle="--", linewidth=1.5)
    for row in rows:
        if row["status"] == "reverted":
            ax2.annotate(
                "REV",
                xy=(row["iteration"], row["metric"]),
                xytext=(0, 8),
                textcoords="offset points",
                ha="center",
                color=COL_REVERTED,
                fontsize=8,
            )
    ax2.set_xlabel("Iteration")
    ax2.set_ylabel("Median runtime (s)")
    ax2.set_xticks(xs)
    ax2.set_xticklabels(labels)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.legend(loc="upper right", frameon=True, edgecolor="black")

    out_png = os.path.join(SCRIPT_DIR, "results.png")
    out_pdf = os.path.join(SCRIPT_DIR, "results.pdf")
    fig.savefig(out_png, dpi=600, bbox_inches="tight", facecolor="white")
    fig.savefig(out_pdf, dpi=600, bbox_inches="tight", facecolor="white")
    print(f"Saved: {out_png}")
    print(f"Saved: {out_pdf}")


if __name__ == "__main__":
    main()
