#!/usr/bin/env python3
"""Publication-quality visualization for the function-fitting autoresearch example.

Panel 1: RMSE convergence over 18 iterations with best-so-far envelope.
Panel 2: Prediction curve vs train/test scatter with residuals.
"""

import csv
import sys
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import numpy as np

# ── constants ─────────────────────────────────────────────────────────────────
BG_DARK   = "#0f1117"
BG_AXES   = "#0f1117"
BG_PANEL  = "#13161f"
COL_BLUE  = "#4a90d9"
COL_RED   = "#d94a4a"
COL_GRAY  = "#6a6d77"
COL_GREEN = "#4adb8b"
COL_AMBER = "#ffcc00"
COL_PINK  = "#e040fb"
COL_ORANGE= "#FF9800"
COL_TEXT  = "#b0b8c8"
COL_WHITE = "#ffffff"
COL_SPINE = "#2a2d37"
TARGET_RMSE = 0.05

# ── helpers ───────────────────────────────────────────────────────────────────

def load_csv(path):
    with open(path) as f:
        reader = csv.DictReader(f)
        return [(float(r["x"]), float(r["y"])) for r in reader]


def load_tsv(path):
    """Return list of dicts from TSV, skipping rows where metric_value is '-'."""
    rows = []
    with open(path) as f:
        reader = csv.DictReader(f, delimiter="\t")
        for r in reader:
            rows.append(r)
    return rows


def ax_style(ax, title, ylabel, xlabel=None):
    """Apply consistent dark-theme styling to an axes."""
    ax.set_facecolor(BG_PANEL)
    ax.set_title(title, fontsize=14, fontweight="bold", color=COL_WHITE, pad=12)
    ax.set_ylabel(ylabel, fontsize=11, color=COL_TEXT)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=11, color=COL_TEXT)
    ax.tick_params(colors=COL_TEXT, labelsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_color(COL_SPINE)
    ax.spines["left"].set_color(COL_SPINE)
    ax.grid(True, alpha=0.15, color=COL_SPINE)


# ── data loading ──────────────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def abspath(name):
    return os.path.join(SCRIPT_DIR, name)


rows = load_tsv(abspath("autoresearch-results.tsv"))

# Parse iteration rows; skip analysis rows (metric_value == "-")
iters_all = []   # (iter_num, rmse, status)
for r in rows:
    mv = r["metric_value"].strip()
    if mv == "-":
        continue
    iters_all.append((int(r["iteration"]), float(mv), r["status"].strip()))

# Build best-so-far envelope (monotonically non-increasing)
best_so_far = []
current_best = None
for (it, rmse, status) in iters_all:
    if current_best is None:
        current_best = rmse
    elif status == "improved" or status == "baseline":
        current_best = min(current_best, rmse)
    best_so_far.append((it, current_best))

all_iters   = [t[0] for t in iters_all]
all_rmses   = [t[1] for t in iters_all]
all_statuses= [t[2] for t in iters_all]

# ── figure setup ──────────────────────────────────────────────────────────────

fig, (ax1, ax2) = plt.subplots(
    2, 1,
    figsize=(12, 10),
    gridspec_kw={"height_ratios": [1, 1], "hspace": 0.38},
)
fig.patch.set_facecolor(BG_DARK)
fig.suptitle(
    "Function Fitting — Autoresearch Loop Results",
    fontsize=17, fontweight="bold", color=COL_WHITE, y=0.98,
)

# ── Panel 1: RMSE Convergence ─────────────────────────────────────────────────

ax_style(ax1,
         title="RMSE Convergence — 18 Iterations",
         ylabel="RMSE",
         xlabel="Iteration")

# Scatter by status
status_style = {
    "baseline":  (COL_BLUE,   "o",  80,  "Baseline / kept"),
    "improved":  (COL_BLUE,   "o",  80,  "Baseline / kept"),
    "reverted":  (COL_RED,    "o",  70,  "Reverted"),
    "no_change": (COL_GRAY,   "o",  60,  "No change / analysis"),
    "analysis":  (COL_GRAY,   "o",  60,  "No change / analysis"),
}
# Track which legend entries we've already added
seen_labels = set()
legend_handles = []

for it, rmse, status in iters_all:
    col, marker, size, label = status_style.get(status, (COL_GRAY, "o", 60, status))
    ax1.scatter(it, rmse, color=col, marker=marker, s=size,
                zorder=5, linewidths=0.5, edgecolors="white")
    if label not in seen_labels:
        seen_labels.add(label)
        legend_handles.append(
            mlines.Line2D([], [], color=col, marker=marker, linestyle="None",
                          markersize=7, label=label, markeredgecolor="white",
                          markeredgewidth=0.5)
        )

# Best-so-far green line
bsf_x = [t[0] for t in best_so_far]
bsf_y = [t[1] for t in best_so_far]
ax1.plot(bsf_x, bsf_y, color=COL_GREEN, linewidth=2.2, zorder=4,
         linestyle="-", label="Best so far")
legend_handles.append(
    mlines.Line2D([], [], color=COL_GREEN, linewidth=2.2, label="Best so far")
)

# Target dashed line
ax1.axhline(TARGET_RMSE, color=COL_AMBER, linestyle="--", linewidth=1.5,
            alpha=0.85, zorder=3)
legend_handles.append(
    mlines.Line2D([], [], color=COL_AMBER, linestyle="--", linewidth=1.5,
                  label=f"Target RMSE = {TARGET_RMSE}")
)

# Annotate baseline
baseline_rmse = iters_all[0][1]
ax1.annotate(
    f"Baseline\n{baseline_rmse:.2f}",
    xy=(0, baseline_rmse),
    xytext=(1.2, baseline_rmse - 0.28),
    fontsize=9, color=COL_TEXT,
    arrowprops=dict(arrowstyle="->", color=COL_GRAY, lw=1.0),
)

# Annotate final best (iter 16, 0.0344)
best_iter, best_rmse = 16, 0.0344
ax1.annotate(
    f"Best: {best_rmse:.4f}\n(-98.4%)",
    xy=(best_iter, best_rmse),
    xytext=(best_iter - 5, best_rmse + 0.12),
    fontsize=9, color=COL_GREEN, fontweight="bold",
    arrowprops=dict(arrowstyle="->", color=COL_GREEN, lw=1.0),
)

# Mark PIVOT iterations (first big drop: iter 1; CV-optimized: iter 7; irrational freqs: iter 16)
pivots = [
    (1,  "PIVOT\n4-freq Fourier",  (1.5,  0.18)),
    (7,  "PIVOT\nCV-optimized",    (5.0,  0.18)),
    (16, "PIVOT\n1/√2, √2 freqs",  (13.5, 0.18)),
]
for pit, plabel, (tx, ty) in pivots:
    rmse_at = next(r for (i, r, _) in iters_all if i == pit)
    ax1.annotate(
        plabel,
        xy=(pit, rmse_at),
        xytext=(tx, ty),
        fontsize=7.5, color=COL_AMBER, alpha=0.9,
        arrowprops=dict(arrowstyle="->", color=COL_AMBER, lw=0.8),
    )

ax1.set_ylim(bottom=-0.05)
ax1.set_xticks(all_iters)
ax1.set_xticklabels([str(i) for i in all_iters], fontsize=8.5, color=COL_TEXT)
ax1.legend(handles=legend_handles, loc="upper right", fontsize=9,
           facecolor="#1a1d27", edgecolor=COL_SPINE, labelcolor=COL_TEXT,
           framealpha=0.85)

# ── Panel 2: Function Fit vs Data ─────────────────────────────────────────────

ax_style(ax2,
         title="Prediction vs Ground Truth",
         ylabel="y",
         xlabel="x")

# Import predict from the same directory
sys.path.insert(0, SCRIPT_DIR)
from predict import predict

train = load_csv(abspath("train_data.csv"))
test  = load_csv(abspath("test_data.csv"))

train_x = np.array([p[0] for p in train])
train_y = np.array([p[1] for p in train])
test_x  = np.array([p[0] for p in test])
test_y  = np.array([p[1] for p in test])

# Dense prediction curve
xs_dense = np.linspace(-3, 3, 600)
ys_pred  = np.array([predict(float(x)) for x in xs_dense])

# Residuals: thin gray vertical lines from test points to prediction curve
# Interpolate predicted y at each test x
test_pred_y = np.array([predict(float(x)) for x in test_x])
for tx, ty, tp in zip(test_x, test_y, test_pred_y):
    ax2.plot([tx, tx], [ty, tp], color=COL_GRAY, linewidth=0.7, alpha=0.55, zorder=2)

# Scatter train
ax2.scatter(train_x, train_y, color=COL_BLUE, alpha=0.40, s=14,
            label="Train data", zorder=3, linewidths=0)

# Scatter test
ax2.scatter(test_x, test_y, color=COL_ORANGE, alpha=0.75, s=35,
            marker="x", linewidths=1.2, label="Test data", zorder=4)

# Prediction curve
ax2.plot(xs_dense, ys_pred, color=COL_PINK, linewidth=2.0, zorder=5,
         label=f"Prediction (RMSE = {best_rmse:.4f})")

ax2.legend(loc="upper left", fontsize=9, facecolor="#1a1d27",
           edgecolor=COL_SPINE, labelcolor=COL_TEXT, framealpha=0.85)

# ── save ──────────────────────────────────────────────────────────────────────

out_path = abspath("results.png")
plt.savefig(out_path, dpi=200, facecolor=BG_DARK, bbox_inches="tight")
print(f"Saved: {out_path}")


if __name__ == "__main__":
    pass  # script runs at module level above for direct execution
