"""Generate taxonomy coverage visualization for the literature review research."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# ── Iteration data (real search progression) ─────────────────────────────────
iterations = list(range(9))
iter_labels = [
    "Iter 0\n(seed)",
    "Iter 1\n(weight)",
    "Iter 2\n(muscle)",
    "Iter 3\n(cardio)",
    "Iter 4\n(hormone)",
    "Iter 5\n(sleep)",
    "Iter 6\n(metabolic)",
    "Iter 7\n(circadian)",
    "Iter 8\n(adherence)",
]

# Coverage progression (categories with ≥2 papers)
coverage_fracs = [2/8, 3/8, 5/8, 5/8, 6/8, 7/8, 7/8, 7/8, 8/8]
coverage_pcts = [f * 100 for f in coverage_fracs]

# Cumulative papers found
cum_papers = [3, 7, 10, 12, 13, 16, 18, 19, 21]

# Papers per category (final state)
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
papers_per_cat = [4, 4, 3, 2, 3, 2, 2, 2]

# ── Figure setup ─────────────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.patch.set_facecolor("#0f1117")
fig.suptitle(
    "Literature Review: Morning vs Evening Exercise\nAuto-Research Loop Results",
    fontsize=18, fontweight="bold", color="white", y=0.98,
)

# ── Chart 1: Coverage trajectory ─────────────────────────────────────────────
ax1 = axes[0, 0]
ax1.fill_between(iterations, coverage_pcts, alpha=0.3, color="#4adb8b")
ax1.plot(iterations, coverage_pcts, "o-", color="#4adb8b", linewidth=2.5, markersize=8)
ax1.axhline(y=100, color="#ffcc00", linestyle="--", linewidth=1.5, alpha=0.8, label="Target: 100%")

for i, pct in enumerate(coverage_pcts):
    ax1.annotate(f"{pct:.0f}%", xy=(i, pct), xytext=(0, 10),
                 textcoords="offset points", ha="center", fontsize=9,
                 color="white", fontweight="bold")

ax1.set_xticks(iterations)
ax1.set_xticklabels(iter_labels, fontsize=8, color="#b0b8c8")
ax1.set_ylabel("Taxonomy Coverage (%)", fontsize=12, color="#b0b8c8")
ax1.set_title("Coverage Progression", fontsize=14, fontweight="bold", color="white")
ax1.set_ylim(0, 115)
ax1.set_facecolor("#0f1117")
ax1.tick_params(colors="#b0b8c8")
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.spines["bottom"].set_color("#2a2d37")
ax1.spines["left"].set_color("#2a2d37")
ax1.legend(loc="lower right", fontsize=10, facecolor="#1a1d27", edgecolor="#2a2d37", labelcolor="white")

# ── Chart 2: Cumulative papers ───────────────────────────────────────────────
ax2 = axes[0, 1]
ax2.bar(iterations, cum_papers, color="#4a90d9", width=0.6, edgecolor="#1a1d27", linewidth=1)
for i, n in enumerate(cum_papers):
    ax2.text(i, n + 0.3, str(n), ha="center", fontsize=10, fontweight="bold", color="white")

ax2.set_xticks(iterations)
ax2.set_xticklabels(iter_labels, fontsize=8, color="#b0b8c8")
ax2.set_ylabel("Cumulative Papers", fontsize=12, color="#b0b8c8")
ax2.set_title("Papers Discovered per Iteration", fontsize=14, fontweight="bold", color="white")
ax2.set_facecolor("#0f1117")
ax2.tick_params(colors="#b0b8c8")
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["bottom"].set_color("#2a2d37")
ax2.spines["left"].set_color("#2a2d37")

# ── Chart 3: Papers per taxonomy category ────────────────────────────────────
ax3 = axes[1, 0]
y_pos = np.arange(len(categories))
colors = ["#4adb8b" if n >= 2 else "#d94a4a" for n in papers_per_cat]
bars = ax3.barh(y_pos, papers_per_cat, color=colors, height=0.6, edgecolor="#1a1d27", linewidth=1)
ax3.axvline(x=2, color="#ffcc00", linestyle="--", linewidth=1.5, alpha=0.8, label="Min threshold: 2")

for i, n in enumerate(papers_per_cat):
    ax3.text(n + 0.1, i, str(n), va="center", fontsize=11, fontweight="bold", color="white")

ax3.set_yticks(y_pos)
ax3.set_yticklabels(categories, fontsize=10, color="#b0b8c8")
ax3.set_xlabel("Number of Papers", fontsize=12, color="#b0b8c8")
ax3.set_title("Final Taxonomy Coverage", fontsize=14, fontweight="bold", color="white")
ax3.set_facecolor("#0f1117")
ax3.tick_params(colors="#b0b8c8")
ax3.spines["top"].set_visible(False)
ax3.spines["right"].set_visible(False)
ax3.spines["bottom"].set_color("#2a2d37")
ax3.spines["left"].set_color("#2a2d37")
ax3.legend(loc="lower right", fontsize=10, facecolor="#1a1d27", edgecolor="#2a2d37", labelcolor="white")
ax3.invert_yaxis()

# ── Chart 4: Morning vs Evening verdict summary ─────────────────────────────
ax4 = axes[1, 1]
outcomes = [
    "Abdominal Fat (♀)",
    "Weight Loss Habit",
    "Muscle Strength",
    "Muscle Hypertrophy",
    "Blood Pressure (HTN)",
    "Insulin Sensitivity",
    "Sleep Disruption Risk",
    "Circadian Alignment",
]
# -1 = morning better, +1 = evening better, 0 = neutral/equal
scores = [-1, -1, 1, 1, 1, 1, 0, 0]
colors_verdict = ["#ff9944" if s < 0 else "#4a90d9" if s > 0 else "#6a6d77" for s in scores]
labels_verdict = ["Morning" if s < 0 else "Evening" if s > 0 else "Neither" for s in scores]

y_pos2 = np.arange(len(outcomes))
bars2 = ax4.barh(y_pos2, scores, color=colors_verdict, height=0.6, edgecolor="#1a1d27", linewidth=1)
ax4.axvline(x=0, color="#2a2d37", linewidth=2)

for i, (s, lbl) in enumerate(zip(scores, labels_verdict)):
    x_pos = s + 0.05 if s >= 0 else s - 0.05
    ha = "left" if s >= 0 else "right"
    ax4.text(x_pos, i, lbl, va="center", ha=ha, fontsize=10, fontweight="bold", color="white")

ax4.set_yticks(y_pos2)
ax4.set_yticklabels(outcomes, fontsize=10, color="#b0b8c8")
ax4.set_xlim(-1.5, 1.5)
ax4.set_xticks([-1, 0, 1])
ax4.set_xticklabels(["Morning ←", "Neutral", "→ Evening"], fontsize=10, color="#b0b8c8")
ax4.set_title("Evidence Direction by Outcome", fontsize=14, fontweight="bold", color="white")
ax4.set_facecolor("#0f1117")
ax4.tick_params(colors="#b0b8c8")
ax4.spines["top"].set_visible(False)
ax4.spines["right"].set_visible(False)
ax4.spines["bottom"].set_color("#2a2d37")
ax4.spines["left"].set_color("#2a2d37")
ax4.invert_yaxis()

plt.tight_layout(pad=2.0, rect=[0, 0, 1, 0.95])
out = "/Users/woojin/Desktop/02_Areas/01_Codes_automation/14_auto-research-skill/examples/literature-review/results.png"
plt.savefig(out, dpi=150, facecolor="#0f1117", bbox_inches="tight")
print(f"Saved: {out}")
