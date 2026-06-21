#!/usr/bin/env python3
"""Publication-quality visualization for the function-fitting autoresearch example.

Panel A: RMSE convergence over iterations with best-so-far envelope.
Panel B: Prediction curve vs train/test scatter with residuals.

Uses /scientific-visualization skill style (rcparams, Pretendard/Arial, DPI 600).
"""

import csv
import math
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np

# ── Load scientific-visualization rcparams (embedded in scripts/style_presets.py) ──
_SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scripts')
sys.path.insert(0, _SCRIPTS_DIR)
from style_presets import rcparams
rcparams()

# ── Constants ────────────────────────────────────────────────────────────────
TARGET_RMSE = 0.05
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Okabe-Ito palette
COL_KEPT = "#0072B2"      # Blue
COL_REVERTED = "#D55E00"  # Vermillion
COL_GRAY = "#BBBBBB"      # Gray
COL_BEST = "#009E73"      # Bluish Green
COL_TARGET = "#E69F00"    # Orange
COL_PRED = "#CC79A7"      # Reddish Purple
COL_TRAIN = "#56B4E9"     # Sky Blue
COL_TEST = "#D55E00"      # Vermillion


def abspath(name):
    return os.path.join(SCRIPT_DIR, name)


def load_csv(path):
    with open(path) as f:
        reader = csv.DictReader(f)
        return [(float(r["x"]), float(r["y"])) for r in reader]


def load_tsv(path):
    rows = []
    with open(path) as f:
        reader = csv.DictReader(f, delimiter="\t")
        for r in reader:
            rows.append(r)
    return rows


# ── Data Loading ─────────────────────────────────────────────────────────────
rows = load_tsv(abspath("autoresearch-results.tsv"))

iters_all = []  # (iter_num, rmse, status)
for r in rows:
    mv = r["metric_value"].strip()
    if mv == "-":
        continue
    iters_all.append((int(r["iteration"]), float(mv), r["status"].strip()))

# Best-so-far envelope (monotonically non-increasing)
best_so_far = []
current_best = None
for (it, rmse, status) in iters_all:
    if current_best is None:
        current_best = rmse
    elif status in ("kept", "improved", "baseline"):
        current_best = min(current_best, rmse)
    best_so_far.append((it, current_best))

all_iters = [t[0] for t in iters_all]
all_rmses = [t[1] for t in iters_all]
all_statuses = [t[2] for t in iters_all]

# ── Figure Setup ─────────────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(
    2, 1,
    figsize=(10, 8),
    gridspec_kw={"height_ratios": [1, 1], "hspace": 0.45},
)

# Panel labels (A, B)
ax1.text(-0.08, 1.08, "A", transform=ax1.transAxes, fontsize=16, fontweight="bold", va="top")
ax2.text(-0.08, 1.08, "B", transform=ax2.transAxes, fontsize=16, fontweight="bold", va="top")

# ── Panel A: RMSE Convergence ────────────────────────────────────────────────
legend_handles = []

# Scatter by status
for it, rmse, status in iters_all:
    if status in ("baseline", "kept", "improved"):
        col, label = COL_KEPT, "Kept"
    elif status == "reverted":
        col, label = COL_REVERTED, "Reverted"
    else:
        col, label = COL_GRAY, "No change"
    ax1.scatter(it, rmse, color=col, s=50, zorder=5, edgecolors="black", linewidths=0.5)

# Legend entries (manual to avoid duplicates)
legend_handles.append(mlines.Line2D([], [], color=COL_KEPT, marker="o", linestyle="None",
                                     markersize=6, label="Kept", markeredgecolor="black", markeredgewidth=0.5))
legend_handles.append(mlines.Line2D([], [], color=COL_REVERTED, marker="o", linestyle="None",
                                     markersize=6, label="Reverted", markeredgecolor="black", markeredgewidth=0.5))

# Best-so-far envelope
bsf_x = [t[0] for t in best_so_far]
bsf_y = [t[1] for t in best_so_far]
ax1.plot(bsf_x, bsf_y, color=COL_BEST, linewidth=2, zorder=4)
legend_handles.append(mlines.Line2D([], [], color=COL_BEST, linewidth=2, label="Best so far"))

# Target line
ax1.axhline(TARGET_RMSE, color=COL_TARGET, linestyle="--", linewidth=1.5, zorder=3)
legend_handles.append(mlines.Line2D([], [], color=COL_TARGET, linestyle="--", linewidth=1.5,
                                     label=f"Target (RMSE = {TARGET_RMSE})"))

# Annotations
baseline_rmse = iters_all[0][1]
ax1.annotate(f"Baseline: {baseline_rmse:.2f}",
             xy=(0, baseline_rmse), xytext=(2.5, baseline_rmse - 0.3),
             fontsize=10, arrowprops=dict(arrowstyle="->", color="black", lw=0.8))

best_rmse = min(r for (_, r, s) in iters_all if s in ("baseline", "kept", "improved"))
best_iter = next(i for (i, r, s) in iters_all if r == best_rmse)
ax1.annotate(f"Best: {best_rmse:.4f}",
             xy=(best_iter, best_rmse), xytext=(best_iter - 6, best_rmse + 0.15),
             fontsize=10, fontweight="bold", color=COL_BEST,
             arrowprops=dict(arrowstyle="->", color=COL_BEST, lw=0.8))

ax1.set_xlabel("Iteration")
ax1.set_ylabel("RMSE")
ax1.set_xlim(-0.5, max(all_iters) + 0.5)
ax1.set_ylim(-0.05, baseline_rmse + 0.15)

# Legend with colored text (Restraint 5)
leg1 = ax1.legend(handles=legend_handles, loc="upper right", frameon=True,
                  edgecolor="black", framealpha=1)
legend_colors = [COL_KEPT, COL_REVERTED, COL_BEST, COL_TARGET]
for i, text in enumerate(leg1.get_texts()):
    text.set_color(legend_colors[i])

# ── Panel B: Function Fit vs Data ────────────────────────────────────────────
sys.path.insert(0, SCRIPT_DIR)
from predict import predict

train = load_csv(abspath("train_data.csv"))
test = load_csv(abspath("test_data.csv"))

train_x = np.array([p[0] for p in train])
train_y = np.array([p[1] for p in train])
test_x = np.array([p[0] for p in test])
test_y = np.array([p[1] for p in test])

# Dense prediction curve
xs_dense = np.linspace(-3, 3, 600)
ys_pred = np.array([predict(float(x)) for x in xs_dense])

# Residuals
test_pred_y = np.array([predict(float(x)) for x in test_x])
for tx, ty_true, ty_pred in zip(test_x, test_y, test_pred_y):
    ax2.plot([tx, tx], [ty_true, ty_pred], color=COL_GRAY, linewidth=0.6, zorder=1)

# Scatter + prediction line
ax2.scatter(train_x, train_y, s=15, alpha=0.4, color=COL_TRAIN, label="Train data", zorder=2)
ax2.scatter(test_x, test_y, s=35, marker="x", color=COL_TEST, linewidths=1.2,
            label="Test data", zorder=3)
ax2.plot(xs_dense, ys_pred, color=COL_PRED, linewidth=1.8,
         label=f"Prediction (RMSE = {best_rmse:.4f})", zorder=4)

ax2.set_xlabel("x")
ax2.set_ylabel("y")
ax2.set_xlim(-3, 3)
ax2.set_ylim(-1.0, 1.5)

# Legend with colored text (Restraint 5)
leg2 = ax2.legend(loc="upper right", frameon=True, edgecolor="black", framealpha=1)
leg2_colors = [COL_TRAIN, COL_TEST, COL_PRED]
for i, text in enumerate(leg2.get_texts()):
    text.set_color(leg2_colors[i])

# ── Save (Restraint 7: DPI > 500) ───────────────────────────────────────────
fig.tight_layout(pad=1.5)
output_path = abspath("results.png")
fig.savefig(output_path, dpi=600, bbox_inches="tight", facecolor="white")
fig.savefig(abspath("results.pdf"), dpi=600, bbox_inches="tight", facecolor="white")
print(f"Saved: {output_path}")
