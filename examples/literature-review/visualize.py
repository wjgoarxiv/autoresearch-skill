"""Generate taxonomy coverage visualization for the literature review research."""

import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

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

# ── Iteration data ────────────────────────────────────────────────────────────
iterations = list(range(5))
iter_labels = [
    "Iter 0\n(seed)",
    "Iter 1\n(weight+\nmetabolic)",
    "Iter 2\n(cardio+\nhormonal)",
    "Iter 3\n(sleep+\nmetabolic)",
    "Iter 4\n(circadian+\nadherence)",
]

coverage_fracs = [2/8, 3/8, 4/8, 6/8, 8/8]
coverage_pcts  = [f * 100 for f in coverage_fracs]
cum_papers     = [3, 8, 16, 20, 25]

categories = [
    "Weight/Fat Loss",
    "Muscle Performance",
    "Cardiovascular",
    "Hormonal Response",
    "Sleep Quality",
    "Metabolic Health",
    "Circadian Rhythm",
    "Adherence",
]
papers_per_cat = [4, 2, 3, 3, 3, 2, 2, 3]

outcomes = [
    "Abdominal Fat (♀)",
    "Weight Loss Overall",
    "Muscle Strength",
    "Blood Pressure (HTN)",
    "Insulin Sensitivity",
    "Fat Oxidation (acute)",
    "Sleep Quality",
    "Circadian Alignment",
]
# -1 = morning better, +1 = evening better, 0 = neutral/equal
scores = [-1, 0, 1, 1, 1, -1, 0, 0]

# ── Figure: 2x2, but only A (top-left) and B (top-right) carry panel labels ──
fig, axes = plt.subplots(2, 2, figsize=(16, 12), facecolor="white")

panel_labels = ["A", "B", "C", "D"]
for ax, lbl in zip(axes.flat, panel_labels):
    ax.text(-0.10, 1.05, lbl, transform=ax.transAxes,
            fontsize=14, fontweight="bold", va="top", ha="left")

# ── Panel A: Coverage trajectory ─────────────────────────────────────────────
ax_A = axes[0, 0]
ax_A.fill_between(iterations, coverage_pcts, alpha=0.15, color=OKI_GREEN)
ax_A.plot(iterations, coverage_pcts, "o-", color=OKI_GREEN, linewidth=2.5, markersize=8)
ax_A.axhline(y=100, color=OKI_ORANGE, linestyle="--", linewidth=1.5,
             alpha=0.9, label="Target: 100%")

for i, pct in enumerate(coverage_pcts):
    ax_A.annotate(f"{pct:.0f}%", xy=(i, pct), xytext=(0, 10),
                  textcoords="offset points", ha="center", fontsize=9,
                  color="black", fontweight="bold")

ax_A.set_xticks(iterations)
ax_A.set_xticklabels(iter_labels, fontsize=8)
ax_A.set_ylabel("Taxonomy coverage (%)")
ax_A.set_ylim(0, 115)
ax_A.set_facecolor("white")
ax_A.spines["top"].set_visible(False)
ax_A.spines["right"].set_visible(False)

leg_A = ax_A.legend(loc="lower right", framealpha=1, edgecolor="black", fontsize=9)
for text, color in zip(leg_A.get_texts(), [OKI_ORANGE]):
    text.set_color(color)

# ── Panel B: Cumulative papers ────────────────────────────────────────────────
ax_B = axes[0, 1]
ax_B.bar(iterations, cum_papers, color=OKI_BLUE, width=0.6,
         edgecolor="white", linewidth=1.2)
for i, n in enumerate(cum_papers):
    ax_B.text(i, n + 0.3, str(n), ha="center", fontsize=10,
              fontweight="bold", color="black")

ax_B.set_xticks(iterations)
ax_B.set_xticklabels(iter_labels, fontsize=8)
ax_B.set_ylabel("Cumulative papers")
ax_B.set_facecolor("white")
ax_B.spines["top"].set_visible(False)
ax_B.spines["right"].set_visible(False)

# ── Panel C: Papers per taxonomy category ────────────────────────────────────
ax_C = axes[1, 0]
y_pos = np.arange(len(categories))
cat_colors = [OKI_GREEN if n >= 2 else OKI_RED for n in papers_per_cat]
ax_C.barh(y_pos, papers_per_cat, color=cat_colors, height=0.6,
          edgecolor="white", linewidth=1.2)
ax_C.axvline(x=2, color=OKI_ORANGE, linestyle="--", linewidth=1.5,
             alpha=0.9, label="Min threshold: 2")

for i, n in enumerate(papers_per_cat):
    ax_C.text(n + 0.1, i, str(n), va="center", fontsize=11,
              fontweight="bold", color="black")

ax_C.set_yticks(y_pos)
ax_C.set_yticklabels(categories, fontsize=10)
ax_C.set_xlabel("Number of papers")
ax_C.set_facecolor("white")
ax_C.spines["top"].set_visible(False)
ax_C.spines["right"].set_visible(False)
ax_C.invert_yaxis()

leg_C = ax_C.legend(loc="lower right", framealpha=1, edgecolor="black", fontsize=9)
for text, color in zip(leg_C.get_texts(), [OKI_ORANGE]):
    text.set_color(color)

# ── Panel D: Evidence direction ───────────────────────────────────────────────
ax_D = axes[1, 1]
verdict_colors = [OKI_ORANGE if s < 0 else OKI_BLUE if s > 0 else OKI_GRAY
                  for s in scores]
verdict_labels = ["Morning" if s < 0 else "Evening" if s > 0 else "Neither"
                  for s in scores]

y_pos2 = np.arange(len(outcomes))
ax_D.barh(y_pos2, scores, color=verdict_colors, height=0.6,
          edgecolor="white", linewidth=1.2)
ax_D.axvline(x=0, color="black", linewidth=1.5, alpha=0.3)

for i, (s, lbl) in enumerate(zip(scores, verdict_labels)):
    x_pos = s + 0.05 if s >= 0 else s - 0.05
    ha = "left" if s >= 0 else "right"
    ax_D.text(x_pos, i, lbl, va="center", ha=ha, fontsize=10,
              fontweight="bold", color="black")

ax_D.set_yticks(y_pos2)
ax_D.set_yticklabels(outcomes, fontsize=10)
ax_D.set_xlim(-1.5, 1.5)
ax_D.set_xticks([-1, 0, 1])
ax_D.set_xticklabels(["Morning ←", "Neutral", "→ Evening"], fontsize=10)
ax_D.set_facecolor("white")
ax_D.spines["top"].set_visible(False)
ax_D.spines["right"].set_visible(False)
ax_D.invert_yaxis()

plt.tight_layout(pad=2.0)

base = os.path.dirname(os.path.abspath(__file__))
png_out = os.path.join(base, "results.png")
pdf_out = os.path.join(base, "results.pdf")
plt.savefig(png_out, dpi=600, bbox_inches="tight")
plt.savefig(pdf_out, dpi=600, bbox_inches="tight")
print(f"Saved: {png_out}")
print(f"Saved: {pdf_out}")
