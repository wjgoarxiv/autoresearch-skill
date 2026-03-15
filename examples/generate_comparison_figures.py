"""
Generate 6 individual figures for the 3x2 README comparison table.
Rows: Code Optimization, Literature Review, Prompt Optimization
Cols: Without autoresearch-skill, With autoresearch-skill
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib import font_manager
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent / "comparison_figures"
OUT.mkdir(exist_ok=True)


def setup_rcparams():
    rcParams['figure.figsize'] = 5, 4
    rcParams['font.family'] = 'sans-serif'

    available_fonts = set([f.name for f in font_manager.fontManager.ttflist])
    if 'Pretendard' in available_fonts:
        rcParams['font.sans-serif'] = ['Pretendard']
    elif 'Arial' in available_fonts:
        rcParams['font.sans-serif'] = ['Arial']
    else:
        print("Note: Arial and Pretendard not installed. Using default font.")

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


setup_rcparams()

BLUE = "#3274A1"
RED = "#C03D3E"
GREEN = "#2CA02C"
GOLD = "#D4A017"
GRAY = "#7F7F7F"


# ══════════════════════════════════════════════════════════════════════════════
# 1. Code Optimization — WITHOUT
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots()
ax.bar(["Quicksort\n(single attempt)"], [2.40], color=RED, width=0.45, edgecolor="black", linewidth=0.8)
ax.axhline(y=0.5, color=GOLD, linestyle="--", linewidth=1.5, label="Target: < 0.5 s")
ax.text(0, 2.48, "2.40 s", ha="center", fontsize=15, fontweight="bold", color=RED)
ax.set_ylabel("Median Time (s)")
ax.set_title("Code Optimization")
ax.set_ylim(0, 3.0)
ax.legend(loc="upper right", fontsize=11)
fig.tight_layout()
fig.savefig(OUT / "code_without.png", dpi=200, bbox_inches="tight")
plt.close(fig)

# ══════════════════════════════════════════════════════════════════════════════
# 2. Code Optimization — WITH
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots()
code_labels = ["v0", "v1", "v2", "v3", "v4", "v5", "v6", "v7"]
code_medians = [2.40, 1.88, 1.73, 1.69, 1.95, 0.98, 0.75, 0.18]
code_kept = [True, True, True, True, False, True, True, True]
colors = [BLUE if k else RED for k in code_kept]

ax.bar(range(len(code_labels)), code_medians, color=colors, width=0.6,
       edgecolor="black", linewidth=0.8)

best = []
cur = code_medians[0]
for m, k in zip(code_medians, code_kept):
    if k and m < cur:
        cur = m
    best.append(cur)
ax.plot(range(len(code_labels)), best, "o-", color=GREEN, linewidth=2, markersize=5, zorder=5,
        label="Best so far")

ax.axhline(y=0.5, color=GOLD, linestyle="--", linewidth=1.5, label="Target")
ax.set_xticks(range(len(code_labels)))
ax.set_xticklabels(code_labels)
ax.set_ylabel("Median Time (s)")
ax.set_xlabel("Iteration")
ax.set_title("Code Optimization")
ax.set_ylim(0, 3.0)
ax.annotate("0.75 s\n(\u221269%)", xy=(6, 0.75), xytext=(4.5, 1.4),
            fontsize=11, fontweight="bold", color=GREEN,
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.5))
ax.legend(loc="upper right", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "code_with.png", dpi=200, bbox_inches="tight")
plt.close(fig)

# ══════════════════════════════════════════════════════════════════════════════
# 3. Literature Review — WITHOUT
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots()
cats = ["Weight/Fat", "Muscle", "Cardio", "Hormonal", "Sleep", "Metabolic", "Circadian", "Adherence"]
manual = [1, 1, 0, 0, 1, 0, 0, 0]
bar_colors = [RED if n < 2 else GREEN for n in manual]
ax.barh(range(len(cats)), manual, color=bar_colors, height=0.55, edgecolor="black", linewidth=0.8)
ax.axvline(x=2, color=GOLD, linestyle="--", linewidth=1.5, label="Min: 2 papers")
ax.set_yticks(range(len(cats)))
ax.set_yticklabels(cats, fontsize=11)
ax.set_xlabel("Papers Found")
ax.set_title("Literature Review")
ax.set_xlim(0, 5)
ax.invert_yaxis()
ax.text(3.2, 6.5, "3 papers\n37% coverage", fontsize=12, fontweight="bold", color=RED)
ax.legend(loc="lower right", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lit_without.png", dpi=200, bbox_inches="tight")
plt.close(fig)

# ══════════════════════════════════════════════════════════════════════════════
# 4. Literature Review — WITH
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots()
auto = [4, 4, 3, 2, 3, 2, 2, 2]
bar_colors = [GREEN if n >= 2 else RED for n in auto]
bars = ax.barh(range(len(cats)), auto, color=bar_colors, height=0.55, edgecolor="black", linewidth=0.8)
ax.axvline(x=2, color=GOLD, linestyle="--", linewidth=1.5, label="Min: 2 papers")
ax.set_yticks(range(len(cats)))
ax.set_yticklabels(cats, fontsize=11)
ax.set_xlabel("Papers Found")
ax.set_title("Literature Review")
ax.set_xlim(0, 5)
ax.invert_yaxis()
for i, n in enumerate(auto):
    ax.text(n + 0.1, i, str(n), va="center", fontsize=11, fontweight="bold")
ax.text(3.2, 6.5, "22 papers\n100% coverage", fontsize=12, fontweight="bold", color=GREEN)
ax.legend(loc="lower right", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "lit_with.png", dpi=200, bbox_inches="tight")
plt.close(fig)

# ══════════════════════════════════════════════════════════════════════════════
# 5. Prompt Optimization — WITHOUT
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots()
ax.bar(["Zero-shot\n(single attempt)"], [68], color=RED, width=0.45, edgecolor="black", linewidth=0.8)
ax.axhline(y=90, color=GOLD, linestyle="--", linewidth=1.5, label="Target: > 90%")
ax.text(0, 70, "68%", ha="center", fontsize=15, fontweight="bold", color=RED)
ax.set_ylabel("Accuracy (%)")
ax.set_title("Prompt Optimization")
ax.set_ylim(0, 105)
ax.legend(loc="upper right", fontsize=11)
fig.tight_layout()
fig.savefig(OUT / "prompt_without.png", dpi=200, bbox_inches="tight")
plt.close(fig)

# ══════════════════════════════════════════════════════════════════════════════
# 6. Prompt Optimization — WITH
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots()
p_labels = ["v0", "v1", "v2", "v3", "v4", "v5", "v6", "v7"]
p_acc = [68, 76, 80, 74, 84, 86, 90, 94]
p_kept = [True, True, True, False, True, True, True, True]
p_colors = [BLUE if k else RED for k in p_kept]

ax.bar(range(len(p_labels)), p_acc, color=p_colors, width=0.6,
       edgecolor="black", linewidth=0.8)

p_best = []
cur = p_acc[0]
for a, k in zip(p_acc, p_kept):
    if k and a > cur:
        cur = a
    p_best.append(cur)
ax.plot(range(len(p_labels)), p_best, "o-", color=GREEN, linewidth=2, markersize=5, zorder=5,
        label="Best so far")

ax.axhline(y=90, color=GOLD, linestyle="--", linewidth=1.5, label="Target")
ax.set_xticks(range(len(p_labels)))
ax.set_xticklabels(p_labels)
ax.set_ylabel("Accuracy (%)")
ax.set_xlabel("Iteration")
ax.set_title("Prompt Optimization")
ax.set_ylim(0, 105)
ax.annotate("94%\n(+26 pp)", xy=(7, 94), xytext=(5.5, 100),
            fontsize=11, fontweight="bold", color=GREEN,
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.5))
ax.legend(loc="lower right", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "prompt_with.png", dpi=200, bbox_inches="tight")
plt.close(fig)

# ══════════════════════════════════════════════════════════════════════════════
# 7. Skill Elaboration — WITHOUT
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots()
cats_skill = ["Streams\n(/15)", "Numbering\n(/15)", "Equipment\n(/8)"]
manual_skill = [4/15*100, 0/15*100, 3/8*100]
ax.bar(cats_skill, manual_skill, color=RED, width=0.45, edgecolor="black", linewidth=0.8)
ax.axhline(y=85, color=GOLD, linestyle="--", linewidth=1.5, label="Target: 85%")
for i, v in enumerate(manual_skill):
    ax.text(i, v + 2, f"{v:.0f}%", ha="center", fontsize=13, fontweight="bold", color=RED)
ax.set_ylabel("Achievement (%)")
ax.set_title("Skill Elaboration (P&ID)")
ax.set_ylim(0, 110)
ax.text(1, 70, "Composite: 18.8%", ha="center", fontsize=12, fontweight="bold", color=RED)
ax.legend(loc="upper right", fontsize=11)
fig.tight_layout()
fig.savefig(OUT / "skill_without.png", dpi=200, bbox_inches="tight")
plt.close(fig)

# ══════════════════════════════════════════════════════════════════════════════
# 8. Skill Elaboration — WITH
# ══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots()
s_labels = ["v0", "v1", "v2", "v3", "v4", "v5", "v6", "v7"]
s_scores = [20.8, 33.3, 57.3, 46.7, 73.3, 82.5, 88.7, 94.5]
s_kept = [True, True, True, False, True, True, True, True]
s_colors = [BLUE if k else RED for k in s_kept]

ax.bar(range(len(s_labels)), s_scores, color=s_colors, width=0.6,
       edgecolor="black", linewidth=0.8)

s_best = []
cur = s_scores[0]
for sc, k in zip(s_scores, s_kept):
    if k and sc > cur:
        cur = sc
    s_best.append(cur)
ax.plot(range(len(s_labels)), s_best, "o-", color=GREEN, linewidth=2, markersize=5, zorder=5,
        label="Best so far")

ax.axhline(y=85, color=GOLD, linestyle="--", linewidth=1.5, label="Target")
ax.set_xticks(range(len(s_labels)))
ax.set_xticklabels(s_labels)
ax.set_ylabel("Composite Score (%)")
ax.set_xlabel("Iteration")
ax.set_title("Skill Elaboration (P&ID)")
ax.set_ylim(0, 105)
ax.annotate("94.5%\n(+73.7 pp)", xy=(7, 94.5), xytext=(5.3, 100),
            fontsize=11, fontweight="bold", color=GREEN,
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.5))
ax.legend(loc="lower right", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "skill_with.png", dpi=200, bbox_inches="tight")
plt.close(fig)

print(f"Generated 8 figures in {OUT}/")
for f in sorted(OUT.glob("*.png")):
    print(f"  {f.name}")
