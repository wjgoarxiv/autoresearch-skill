#!/usr/bin/env python3
"""
Visualization for skill-elaboration example.

Two-panel figure:
  A — Composite score convergence across iterations (from TSV)
  B — Score component breakdown (concept coverage, section structure, depth, specificity)
"""

import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import re
import csv
from matplotlib.patches import Patch
from pathlib import Path

# Scientific visualization style (embedded in scripts/style_presets.py)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scripts'))
from style_presets import rcparams
rcparams()

# ---------------------------------------------------------------------------
# Okabe-Ito palette (colorblind-safe)
# ---------------------------------------------------------------------------
OI_BLUE       = "#0072B2"
OI_ORANGE     = "#E69F00"
OI_GREEN      = "#009E73"
OI_VERMILLION = "#D55E00"
OI_SKY        = "#56B4E9"
OI_PURPLE     = "#CC79A7"

TARGET = 0.85

# ---------------------------------------------------------------------------
# Evaluator components (mirrors evaluate.py logic)
# ---------------------------------------------------------------------------
REQUIRED_CONCEPTS = [
    "process stream", "flow direction", "equipment tag",
    "valve", "pump", "heat exchanger", "vessel", "tank",
    "instrument", "control loop", "line number",
    "P&ID symbol", "process flow diagram",
    "piping", "notation"
]
REQUIRED_SECTIONS = [
    "extraction", "identification", "analysis", "symbol", "stream"
]
SPECIFICITY_MARKERS = [
    r"step\s*\d", r"example", r"tag\s*format", r"iso\s*\d+",
    r"arrow", r"diamond", r"circle", r"rectangle"
]

def compute_components(filepath):
    """Compute the 4 sub-scores from a SKILL.md file."""
    with open(filepath) as f:
        content = f.read().lower()
    concepts = sum(1 for c in REQUIRED_CONCEPTS if c in content) / len(REQUIRED_CONCEPTS)
    headings = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
    heading_text = " ".join(headings).lower()
    sections = sum(1 for s in REQUIRED_SECTIONS if s in heading_text) / len(REQUIRED_SECTIONS)
    depth = min(len(content.split()) / 500, 1.0)
    specificity = sum(1 for m in SPECIFICITY_MARKERS if re.search(m, content)) / len(SPECIFICITY_MARKERS)
    return concepts, sections, depth, specificity

# ---------------------------------------------------------------------------
# Load data from TSV
# ---------------------------------------------------------------------------
tsv_path = Path(__file__).parent / "autoresearch-results.tsv"
iterations = []
scores = []
statuses = []
descriptions = []

with open(tsv_path) as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        iterations.append(int(row['iteration']))
        scores.append(float(row['metric_value']))
        statuses.append(row['status'].strip())
        descriptions.append(row['description'].strip())

labels = [f"v{i}" for i in iterations]
reverted = [s == "reverted" for s in statuses]
x = np.arange(len(iterations))

# ---------------------------------------------------------------------------
# Compute component breakdown for current improved skill
# ---------------------------------------------------------------------------
skill_path = Path(__file__).parent / "improved_skill" / "SKILL.md"
concepts_score, sections_score, depth_score, specificity_score = compute_components(skill_path)

# Also compute for original
orig_path = Path(__file__).parent / "original_skill" / "SKILL.md"
orig_concepts, orig_sections, orig_depth, orig_specificity = compute_components(orig_path)

# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle(
    "Skill Elaboration: P&ID Diagram Analysis",
    fontsize=15, fontweight="bold", y=1.01,
)

# -- Panel A: Composite score convergence ------------------------------------
ax_a = axes[0]
ax_a.text(-0.12, 1.06, "A", transform=ax_a.transAxes,
          fontsize=16, fontweight="bold", va="top")

bar_colors = [OI_VERMILLION if r else OI_BLUE for r in reverted]
valid_scores = [s * 100 for s in scores]
bars = ax_a.bar(x, valid_scores, color=bar_colors,
                width=0.6, zorder=3, edgecolor="white", linewidth=0.5)

ax_a.axhline(TARGET * 100, color=OI_ORANGE, linestyle="--",
             linewidth=1.5, label=f"Target {int(TARGET*100)}%", zorder=4)

for bar, sc in zip(bars, scores):
    ax_a.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1.2,
        f"{sc*100:.1f}%",
        ha="center", va="bottom", fontsize=9,
    )

legend_elements = [
    Patch(facecolor=OI_BLUE,       label="Kept"),
    Patch(facecolor=OI_VERMILLION,  label="Reverted"),
    plt.Line2D([0], [0], color=OI_ORANGE, linestyle="--",
               linewidth=1.5, label=f"Target {int(TARGET*100)}%"),
]
ax_a.legend(handles=legend_elements, loc="lower right")
ax_a.set_xticks(x)
ax_a.set_xticklabels(labels, fontsize=9)
ax_a.set_ylabel("Composite Score (%)")
ax_a.set_title("Score Convergence")
ax_a.set_ylim(0, 110)
ax_a.yaxis.set_minor_locator(ticker.MultipleLocator(5))

# -- Panel B: Component breakdown (original vs improved) ---------------------
ax_b = axes[1]
ax_b.text(-0.12, 1.06, "B", transform=ax_b.transAxes,
          fontsize=16, fontweight="bold", va="top")

comp_labels = ["Concepts\n(35%)", "Sections\n(25%)", "Depth\n(20%)", "Specificity\n(20%)"]
orig_vals = np.array([orig_concepts, orig_sections, orig_depth, orig_specificity]) * 100
improved_vals = np.array([concepts_score, sections_score, depth_score, specificity_score]) * 100

bx = np.arange(len(comp_labels))
width = 0.35

bars_orig = ax_b.bar(bx - width/2, orig_vals, width, color=OI_SKY,
                     label="Original", zorder=3, edgecolor="white", linewidth=0.3)
bars_impr = ax_b.bar(bx + width/2, improved_vals, width, color=OI_GREEN,
                     label="Improved", zorder=3, edgecolor="white", linewidth=0.3)

for bar, val in zip(bars_orig, orig_vals):
    if val > 0:
        ax_b.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                  f"{val:.0f}%", ha="center", va="bottom", fontsize=8)
for bar, val in zip(bars_impr, improved_vals):
    ax_b.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
              f"{val:.0f}%", ha="center", va="bottom", fontsize=8)

ax_b.set_xticks(bx)
ax_b.set_xticklabels(comp_labels, fontsize=9)
ax_b.set_ylabel("Sub-Score (%)")
ax_b.set_title("Component Breakdown")
ax_b.set_ylim(0, 120)
ax_b.yaxis.set_minor_locator(ticker.MultipleLocator(10))
ax_b.legend(loc="upper right")

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
plt.tight_layout()
out = Path(__file__).parent / "results.png"
plt.savefig(out, dpi=600, bbox_inches="tight", facecolor="white")
print(f"Saved: {out}")
plt.close()
