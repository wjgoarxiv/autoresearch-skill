"""
Visualization for skill-elaboration example.

Generates a 2x2 figure summarising how each iteration of the improved
/pdf skill performed on P&ID stream identification.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rcParams, font_manager

# ---------------------------------------------------------------------------
# rcParams (project style)
# ---------------------------------------------------------------------------
rcParams['figure.figsize'] = 5, 4
rcParams['font.family'] = 'sans-serif'
available_fonts = set([f.name for f in font_manager.fontManager.ttflist])
if 'Pretendard' in available_fonts:
    rcParams['font.sans-serif'] = ['Pretendard']
elif 'Arial' in available_fonts:
    rcParams['font.sans-serif'] = ['Arial']
rcParams['axes.labelpad'] = 8
rcParams['xtick.major.pad'] = 7
rcParams['ytick.major.pad'] = 7
rcParams['xtick.minor.visible'] = True
rcParams['ytick.minor.visible'] = True
rcParams['xtick.major.width'] = 1
rcParams['ytick.major.width'] = 1
rcParams['xtick.minor.width'] = 0.5
rcParams['ytick.minor.width'] = 0.5
rcParams['xtick.major.size'] = 5
rcParams['ytick.major.size'] = 5
rcParams['xtick.minor.size'] = 3
rcParams['ytick.minor.size'] = 3
rcParams['xtick.color'] = 'black'
rcParams['ytick.color'] = 'black'
rcParams['font.size'] = 14
rcParams['axes.titlepad'] = 10
rcParams['axes.titleweight'] = 'normal'
rcParams['axes.titlesize'] = 18
rcParams['axes.labelweight'] = 'normal'
rcParams['xtick.labelsize'] = 12
rcParams['ytick.labelsize'] = 12
rcParams['axes.labelsize'] = 16
rcParams['xtick.direction'] = 'in'
rcParams['ytick.direction'] = 'in'

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
BLUE   = "#3274A1"
RED    = "#C03D3E"
GREEN  = "#2CA02C"
GOLD   = "#D4A017"
ORANGE = "#E67E22"

TARGET = 0.85

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
VERSIONS = ["v0", "v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8"]
REVERTED = {"v3"}

# (streams_found, streams_numbered, equipment_found)
PROFILES = {
    "v0": (4,  0,  3),
    "v1": (7,  0,  4),
    "v2": (10, 3,  6),
    "v3": (8,  2,  5),   # reverted — stuck detection L1
    "v4": (11, 7,  7),
    "v5": (12, 10, 7),
    "v6": (13, 11, 8),   # target met
    "v7": (14, 13, 8),   # endgame mode
    "v8": (14, 13, 8),   # last iteration — final polish
}

TOTAL_STREAMS   = 15
TOTAL_EQUIPMENT = 8


def composite(streams, numbered, equipment):
    return (
        0.5 * streams / TOTAL_STREAMS
        + 0.3 * numbered / max(streams, 1)
        + 0.2 * equipment / TOTAL_EQUIPMENT
    )


scores = [composite(*PROFILES[v]) for v in VERSIONS]

# Component contributions (not normalised — raw sub-scores for stacking)
comp_stream    = [0.5 * PROFILES[v][0] / TOTAL_STREAMS          for v in VERSIONS]
comp_numbering = [0.3 * PROFILES[v][1] / max(PROFILES[v][0], 1) for v in VERSIONS]
comp_equip     = [0.2 * PROFILES[v][2] / TOTAL_EQUIPMENT        for v in VERSIONS]

# Best-so-far trajectory (skip reverted versions)
best_so_far = []
running_best = 0.0
for v, s in zip(VERSIONS, scores):
    if v not in REVERTED:
        running_best = max(running_best, s)
    best_so_far.append(running_best)

# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.patch.set_facecolor("white")

x = np.arange(len(VERSIONS))

# ------------------------------------------------------------------
# Chart 1 – Composite score bar chart
# ------------------------------------------------------------------
ax1 = axes[0, 0]
ax1.set_facecolor("white")

bar_colors = [RED if v in REVERTED else BLUE for v in VERSIONS]
bars = ax1.bar(x, [s * 100 for s in scores], color=bar_colors,
               width=0.6, zorder=3)

ax1.axhline(TARGET * 100, color=GOLD, linestyle="--", linewidth=1.5,
            label=f"Target {int(TARGET*100)}%", zorder=4)

for bar, s in zip(bars, scores):
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1.0,
        f"{s:.1%}",
        ha="center", va="bottom", fontsize=10,
    )

ax1.set_xticks(x)
ax1.set_xticklabels(VERSIONS)
ax1.set_ylabel("Composite Score (%)")
ax1.set_title("Composite Score by Iteration")
ax1.set_ylim(0, 105)
ax1.set_xlim(-0.5, len(VERSIONS) - 0.5)

kept_patch    = mpatches.Patch(color=BLUE, label="Kept")
reverted_patch = mpatches.Patch(color=RED,  label="Reverted")
target_line   = plt.Line2D([0], [0], color=GOLD, linestyle="--",
                            linewidth=1.5, label=f"Target {int(TARGET*100)}%")
ax1.legend(handles=[kept_patch, reverted_patch, target_line],
           fontsize=10, framealpha=0.9)

# ------------------------------------------------------------------
# Chart 2 – Score trajectory
# ------------------------------------------------------------------
ax2 = axes[0, 1]
ax2.set_facecolor("white")

ax2.plot(x, [s * 100 for s in scores], color=BLUE, marker="o",
         linewidth=1.8, markersize=6, zorder=3, label="Iteration score")
ax2.plot(x, [s * 100 for s in best_so_far], color=GREEN, marker="s",
         linewidth=1.8, markersize=5, linestyle="--", zorder=3,
         label="Best so far")
ax2.axhline(TARGET * 100, color=GOLD, linestyle="--", linewidth=1.5,
            label=f"Target {int(TARGET*100)}%", zorder=2)

# Annotations
v3_idx = VERSIONS.index("v3")
ax2.annotate(
    "REVERTED",
    xy=(v3_idx, scores[v3_idx] * 100),
    xytext=(v3_idx + 0.4, scores[v3_idx] * 100 + 8),
    arrowprops=dict(arrowstyle="->", color=RED, lw=1.2),
    color=RED, fontsize=9,
)

v6_idx = VERSIONS.index("v6")
ax2.annotate(
    "Target met!",
    xy=(v6_idx, scores[v6_idx] * 100),
    xytext=(v6_idx - 1.1, scores[v6_idx] * 100 + 5),
    arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.2),
    color=GREEN, fontsize=9,
)

v8_idx = VERSIONS.index("v8")
ax2.annotate(
    f"Best: {scores[v8_idx]:.1%}",
    xy=(v8_idx, scores[v8_idx] * 100),
    xytext=(v8_idx - 2.0, scores[v8_idx] * 100 + 4),
    arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.2),
    color=BLUE, fontsize=9,
)

ax2.set_xticks(x)
ax2.set_xticklabels(VERSIONS)
ax2.set_ylabel("Composite Score (%)")
ax2.set_title("Score Trajectory")
ax2.set_ylim(0, 105)
ax2.set_xlim(-0.5, len(VERSIONS) - 0.5)
ax2.legend(fontsize=10, framealpha=0.9)

# ------------------------------------------------------------------
# Chart 3 – Component breakdown stacked bar
# ------------------------------------------------------------------
ax3 = axes[1, 0]
ax3.set_facecolor("white")

b1 = ax3.bar(x, [v * 100 for v in comp_stream],
             color=BLUE, width=0.6, label="Stream Detection", zorder=3)
b2 = ax3.bar(x, [v * 100 for v in comp_numbering],
             bottom=[v * 100 for v in comp_stream],
             color=ORANGE, width=0.6, label="Stream Numbering", zorder=3)
b3 = ax3.bar(x, [v * 100 for v in comp_equip],
             bottom=[(a + b) * 100 for a, b in zip(comp_stream, comp_numbering)],
             color=GREEN, width=0.6, label="Equipment ID", zorder=3)

ax3.axhline(TARGET * 100, color=GOLD, linestyle="--", linewidth=1.5,
            label=f"Target {int(TARGET*100)}%", zorder=4)

ax3.set_xticks(x)
ax3.set_xticklabels(VERSIONS)
ax3.set_ylabel("Score Contribution (%)")
ax3.set_title("Component Breakdown")
ax3.set_ylim(0, 105)
ax3.set_xlim(-0.5, len(VERSIONS) - 0.5)
ax3.legend(fontsize=9, framealpha=0.9)

# ------------------------------------------------------------------
# Chart 4 – Original vs Improved grouped bar
# ------------------------------------------------------------------
ax4 = axes[1, 1]
ax4.set_facecolor("white")

categories  = ["Streams\n(x/15)", "Numbering\n(x/14)", "Equipment\n(x/8)"]
v0_streams,  v0_numbered,  v0_equip  = PROFILES["v0"]
v8_streams,  v8_numbered,  v8_equip  = PROFILES["v8"]

original = [
    v0_streams  / TOTAL_STREAMS * 100,
    v0_numbered / 14            * 100,
    v0_equip    / TOTAL_EQUIPMENT * 100,
]
improved = [
    v8_streams  / TOTAL_STREAMS * 100,
    v8_numbered / 14            * 100,
    v8_equip    / TOTAL_EQUIPMENT * 100,
]

cat_x  = np.arange(len(categories))
width  = 0.35

ax4.bar(cat_x - width / 2, original, width, color=RED,   label="Original (v0)", zorder=3)
ax4.bar(cat_x + width / 2, improved, width, color=GREEN, label="Improved (v8)", zorder=3)

for i, (o, m) in enumerate(zip(original, improved)):
    ax4.text(cat_x[i] - width / 2, o + 1.5, f"{o:.0f}%",
             ha="center", va="bottom", fontsize=9)
    ax4.text(cat_x[i] + width / 2, m + 1.5, f"{m:.0f}%",
             ha="center", va="bottom", fontsize=9)

ax4.set_xticks(cat_x)
ax4.set_xticklabels(categories, fontsize=11)
ax4.set_ylabel("Achievement (%)")
ax4.set_title("Original vs Improved")
ax4.set_ylim(0, 120)
ax4.legend(fontsize=10, framealpha=0.9)

# ------------------------------------------------------------------
# Final layout & save
# ------------------------------------------------------------------
plt.tight_layout(pad=2.5)

from pathlib import Path
OUTPUT_PATH = str(Path(__file__).parent / "results.png")
plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches="tight", facecolor="white")
print(f"Saved: {OUTPUT_PATH}")
plt.close()
