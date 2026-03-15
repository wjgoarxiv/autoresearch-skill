"""Generate performance visualization for the sorting optimization research."""

import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Real benchmark results
results = [
    {"tag": "v0", "label": "Quicksort\n(baseline)", "median": 2.3991, "kept": True},
    {"tag": "v1", "label": "Iterative\nmerge sort", "median": 1.8845, "kept": True},
    {"tag": "v2", "label": "Merge +\ninsertion(32)", "median": 1.7265, "kept": True},
    {"tag": "v3", "label": "Merge +\nbinary ins(64)", "median": 1.6939, "kept": True},
    {"tag": "v4", "label": "Natural\nmerge sort", "median": 1.9504, "kept": False},
    {"tag": "v5", "label": "Radix sort\nbase 256", "median": 0.9817, "kept": True},
    {"tag": "v6", "label": "Radix sort\nbase 65536", "median": 0.7513, "kept": True},
    {"tag": "v7", "label": "sorted()\n[reference]", "median": 0.178, "kept": True},
]

labels = [r["label"] for r in results]
medians = [r["median"] for r in results]
kept = [r["kept"] for r in results]
colors = ["#4a90d9" if k else "#d94a4a" for k in kept]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={"height_ratios": [3, 2]})
fig.patch.set_facecolor("#0f1117")

# ── Chart 1: Bar chart with median times ─────────────────────────────────────
bars = ax1.bar(range(len(labels)), medians, color=colors, width=0.6, edgecolor="#1a1d27", linewidth=1.5)

# Target line
ax1.axhline(y=0.5, color="#ffcc00", linestyle="--", linewidth=1.5, alpha=0.8, label="Target: < 0.5s")

# Value labels on bars
for i, (bar, val) in enumerate(enumerate(medians)):
    ax1.text(i, val + 0.05, f"{val:.3f}s", ha="center", va="bottom",
             fontsize=10, fontweight="bold", color="white")

ax1.set_xticks(range(len(labels)))
ax1.set_xticklabels(labels, fontsize=9, color="#b0b8c8")
ax1.set_ylabel("Median Time (seconds)", fontsize=12, color="#b0b8c8")
ax1.set_title("Sorting Algorithm Optimization — Auto-Research Loop Results",
              fontsize=16, fontweight="bold", color="white", pad=15)
ax1.set_facecolor("#0f1117")
ax1.tick_params(colors="#b0b8c8")
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.spines["bottom"].set_color("#2a2d37")
ax1.spines["left"].set_color("#2a2d37")
ax1.legend(loc="upper right", fontsize=10, facecolor="#1a1d27", edgecolor="#2a2d37",
           labelcolor="white")

# Custom legend for kept/reverted
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor="#4a90d9", label="Kept (improved)"),
    Patch(facecolor="#d94a4a", label="Reverted (no improvement)"),
    plt.Line2D([0], [0], color="#ffcc00", linestyle="--", linewidth=1.5, label="Target: < 0.5s"),
]
ax1.legend(handles=legend_elements, loc="upper right", fontsize=10,
           facecolor="#1a1d27", edgecolor="#2a2d37", labelcolor="white")

# ── Chart 2: Improvement trajectory (best-so-far line) ──────────────────────
iterations = list(range(len(results)))
best_so_far = []
current_best = results[0]["median"]
for r in results:
    if r["kept"] and r["median"] < current_best:
        current_best = r["median"]
    best_so_far.append(current_best)

ax2.plot(iterations, medians, "o-", color="#6a6d77", linewidth=1, markersize=6,
         alpha=0.5, label="Each iteration")
ax2.plot(iterations, best_so_far, "o-", color="#4adb8b", linewidth=2.5, markersize=8,
         label="Best so far", zorder=5)
ax2.axhline(y=0.5, color="#ffcc00", linestyle="--", linewidth=1.5, alpha=0.8)

# Annotate key points
ax2.annotate(f"Baseline\n{results[0]['median']:.2f}s", xy=(0, results[0]["median"]),
             xytext=(0.5, results[0]["median"] + 0.2),
             fontsize=9, color="#b0b8c8", arrowprops=dict(arrowstyle="->", color="#6a6d77"))
ax2.annotate(f"Best pure Python\n{results[6]['median']:.2f}s (-{(1-results[6]['median']/results[0]['median'])*100:.0f}%)",
             xy=(6, results[6]["median"]),
             xytext=(4.5, results[6]["median"] + 0.4),
             fontsize=9, color="#4adb8b", fontweight="bold",
             arrowprops=dict(arrowstyle="->", color="#4adb8b"))
ax2.annotate("REVERTED", xy=(4, results[4]["median"]),
             xytext=(4, results[4]["median"] + 0.3),
             fontsize=8, color="#d94a4a", ha="center",
             arrowprops=dict(arrowstyle="->", color="#d94a4a"))

ax2.set_xticks(iterations)
ax2.set_xticklabels([f"Iter {i}" for i in iterations], fontsize=9, color="#b0b8c8")
ax2.set_ylabel("Median Time (seconds)", fontsize=12, color="#b0b8c8")
ax2.set_xlabel("Iteration", fontsize=12, color="#b0b8c8")
ax2.set_title("Optimization Trajectory — Best-So-Far vs Each Iteration",
              fontsize=14, fontweight="bold", color="white", pad=10)
ax2.set_facecolor("#0f1117")
ax2.tick_params(colors="#b0b8c8")
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["bottom"].set_color("#2a2d37")
ax2.spines["left"].set_color("#2a2d37")
ax2.legend(loc="upper right", fontsize=10, facecolor="#1a1d27", edgecolor="#2a2d37",
           labelcolor="white")

plt.tight_layout(pad=2.0)
out = "/Users/woojin/Desktop/02_Areas/01_Codes_automation/14_auto-research-skill/examples/code-optimization/results.png"
plt.savefig(out, dpi=150, facecolor="#0f1117", bbox_inches="tight")
print(f"Saved: {out}")
