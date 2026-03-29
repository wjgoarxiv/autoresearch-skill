"""Generate performance visualization for the sorting optimization research."""

import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

# Scientific visualization style (045_scientific-visualization skill)
try:
    sys.path.insert(0, os.path.expanduser("~/.claude/skills/045_scientific-visualization/scripts"))
    from style_presets import rcparams
    rcparams()
except ImportError:
    # Fallback: manual rcparams approximating the skill's output
    plt.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": False,
        "font.family": "sans-serif",
    })

# Okabe-Ito color palette
OKI_BLUE   = "#0072B2"
OKI_ORANGE = "#E69F00"
OKI_GREEN  = "#009E73"
OKI_RED    = "#D55E00"
OKI_GRAY   = "#999999"
OKI_LBLUE  = "#56B4E9"
OKI_YELLOW = "#F0E442"

# ── Data ─────────────────────────────────────────────────────────────────────
results = [
    {"tag": "v0",  "label": "Quicksort\n(baseline)",       "median": 2.3991, "kept": True},
    {"tag": "v1",  "label": "Radix sort\nbase 256",        "median": 0.8709, "kept": True},
    {"tag": "v2",  "label": "Radix sort\nbase 65536",      "median": 0.5727, "kept": True},
    {"tag": "v3",  "label": "Micro-opt\nradix 65536",      "median": 0.4979, "kept": True},
    {"tag": "v4",  "label": "Counting\nsort (10M)",        "median": 0.6717, "kept": False},
    {"tag": "v5",  "label": "array module\nfor counts",    "median": 0.6967, "kept": False},
    {"tag": "v6",  "label": "Pre-computed\nhistograms",    "median": 0.4486, "kept": True},
    {"tag": "v7",  "label": "Radix base\n2048 (11-bit)",   "median": 0.7205, "kept": False},
    {"tag": "v8",  "label": "sorted()-based\nradix (2x)",  "median": 0.4226, "kept": True},
    {"tag": "v9",  "label": "Direct\nsorted()",            "median": 0.1920, "kept": True},
    {"tag": "v10", "label": "list.sort()\nin-place",       "median": 0.1847, "kept": True},
    {"tag": "v11", "label": "Hybrid\nbucket+Timsort",      "median": 0.2494, "kept": False},
]

labels  = [r["label"] for r in results]
medians = [r["median"] for r in results]
kept    = [r["kept"] for r in results]
bar_colors = [OKI_BLUE if k else OKI_RED for k in kept]

iterations   = list(range(len(results)))
best_so_far  = []
current_best = results[0]["median"]
for r in results:
    if r["kept"] and r["median"] < current_best:
        current_best = r["median"]
    best_so_far.append(current_best)

# ── Figure ────────────────────────────────────────────────────────────────────
fig, (ax_A, ax_B) = plt.subplots(
    2, 1, figsize=(14, 10),
    gridspec_kw={"height_ratios": [3, 2]},
    facecolor="white",
)

# Panel labels
for ax, lbl in zip([ax_A, ax_B], ["A", "B"]):
    ax.text(-0.07, 1.05, lbl, transform=ax.transAxes,
            fontsize=14, fontweight="bold", va="top", ha="left")

# ── Panel A: bar chart ────────────────────────────────────────────────────────
ax_A.bar(range(len(labels)), medians, color=bar_colors, width=0.6,
         edgecolor="white", linewidth=1.2)
ax_A.axhline(y=0.5, color=OKI_ORANGE, linestyle="--", linewidth=1.5,
             alpha=0.9, label="Target: < 0.5 s")

for i, val in enumerate(medians):
    ax_A.text(i, val + 0.04, f"{val:.3f}s", ha="center", va="bottom",
              fontsize=8, fontweight="bold", color="black", rotation=45)

ax_A.set_xticks(range(len(labels)))
ax_A.set_xticklabels(labels, fontsize=8)
ax_A.set_ylabel("Median time (s)")
ax_A.set_title("Sorting Algorithm Optimization: 1M Random Integers", fontsize=13, fontweight="bold", pad=15)
ax_A.set_facecolor("white")
ax_A.spines["top"].set_visible(False)
ax_A.spines["right"].set_visible(False)

legend_elements = [
    Patch(facecolor=OKI_BLUE,   label="Kept (improved)"),
    Patch(facecolor=OKI_RED,    label="Reverted (no improvement)"),
    plt.Line2D([0], [0], color=OKI_ORANGE, linestyle="--",
               linewidth=1.5, label="Target: < 0.5 s"),
]
leg_A = ax_A.legend(handles=legend_elements, loc="upper right",
                    framealpha=1, edgecolor="black", fontsize=9)
for text, color in zip(leg_A.get_texts(), [OKI_BLUE, OKI_RED, OKI_ORANGE]):
    text.set_color(color)

# ── Panel B: convergence trajectory ──────────────────────────────────────────
ax_B.plot(iterations, medians, "o-", color=OKI_GRAY, linewidth=1,
          markersize=5, alpha=0.6, label="Each iteration")
ax_B.plot(iterations, best_so_far, "o-", color=OKI_GREEN, linewidth=2.5,
          markersize=7, label="Best so far", zorder=5)
ax_B.axhline(y=0.5, color=OKI_ORANGE, linestyle="--", linewidth=1.5, alpha=0.9)

ax_B.annotate(
    f"Baseline\n{results[0]['median']:.2f}s",
    xy=(0, results[0]["median"]),
    xytext=(0.8, results[0]["median"] + 0.15),
    fontsize=9, color="black",
    arrowprops=dict(arrowstyle="->", color=OKI_GRAY),
)

# Best pure Python result
ax_B.annotate(
    f"Best pure Python\n{results[6]['median']:.2f}s "
    f"(-{(1 - results[6]['median']/results[0]['median'])*100:.0f}%)",
    xy=(6, results[6]["median"]),
    xytext=(4.0, results[6]["median"] + 0.55),
    fontsize=9, color=OKI_GREEN, fontweight="bold",
    arrowprops=dict(arrowstyle="->", color=OKI_GREEN),
)

# Best overall
ax_B.annotate(
    f"Best overall\n{results[10]['median']:.3f}s "
    f"(-{(1 - results[10]['median']/results[0]['median'])*100:.0f}%)",
    xy=(10, results[10]["median"]),
    xytext=(8.0, results[10]["median"] + 0.40),
    fontsize=9, color=OKI_BLUE, fontweight="bold",
    arrowprops=dict(arrowstyle="->", color=OKI_BLUE),
)

# Mark reverted iterations
for i, r in enumerate(results):
    if not r["kept"]:
        ax_B.annotate(
            "REV",
            xy=(i, r["median"]),
            xytext=(i, r["median"] + 0.12),
            fontsize=7, color=OKI_RED, ha="center",
            arrowprops=dict(arrowstyle="->", color=OKI_RED, lw=0.8),
        )

ax_B.set_xticks(iterations)
ax_B.set_xticklabels([f"Iter {i}" for i in iterations], fontsize=8)
ax_B.set_ylabel("Median time (s)")
ax_B.set_xlabel("Iteration")
ax_B.set_facecolor("white")
ax_B.spines["top"].set_visible(False)
ax_B.spines["right"].set_visible(False)

leg_B = ax_B.legend(loc="upper right", framealpha=1, edgecolor="black", fontsize=9)
for text, color in zip(leg_B.get_texts(), [OKI_GRAY, OKI_GREEN]):
    text.set_color(color)

plt.tight_layout(pad=2.0)

base = os.path.dirname(os.path.abspath(__file__))
png_out = os.path.join(base, "results.png")
pdf_out = os.path.join(base, "results.pdf")
plt.savefig(png_out, dpi=600, bbox_inches="tight")
plt.savefig(pdf_out, dpi=600, bbox_inches="tight")
print(f"Saved: {png_out}")
print(f"Saved: {pdf_out}")
