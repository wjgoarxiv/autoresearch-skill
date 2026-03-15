"""Generate visualization for the prompt optimization research."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Real evaluation results
versions = ["v0", "v1", "v2", "v3", "v4", "v5", "v6", "v7"]
labels = [
    "Zero-shot\n(baseline)",
    "Category\ndefinitions",
    "3 few-shot\nexamples",
    "Chain-of-\nthought",
    "5 targeted\nexamples",
    "JSON output\nformat",
    "Decision\nrules",
    "Optimized\nexamples",
]
accuracy = [68.0, 76.0, 80.0, 74.0, 84.0, 86.0, 90.0, 94.0]
correct = [34, 38, 40, 37, 42, 43, 45, 47]
kept = [True, True, True, False, True, True, True, True]

# Error breakdown per category (for stacked bar)
cat_names = ["Billing", "Account", "Bug Report", "Technical", "Returns", "General Inquiry"]
errors_data = {
    "Billing":         [6, 2, 2, 2, 1, 1, 1, 1],
    "Account":         [4, 2, 2, 2, 1, 1, 0, 0],
    "Bug Report":      [4, 4, 4, 3, 2, 1, 1, 1],
    "Technical":       [0, 0, 0, 0, 2, 2, 1, 1],
    "Returns":         [0, 2, 1, 2, 1, 1, 1, 0],
    "General Inquiry": [2, 2, 1, 4, 1, 1, 1, 0],
}

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.patch.set_facecolor("#0f1117")
fig.suptitle(
    "Prompt Optimization: Customer Support Classifier\nAuto-Research Loop Results",
    fontsize=18, fontweight="bold", color="white", y=0.98,
)

# ── Chart 1: Accuracy bar chart ──────────────────────────────────────────────
ax1 = axes[0, 0]
colors = ["#4a90d9" if k else "#d94a4a" for k in kept]
bars = ax1.bar(range(len(labels)), accuracy, color=colors, width=0.6,
               edgecolor="#1a1d27", linewidth=1.5)
ax1.axhline(y=90, color="#ffcc00", linestyle="--", linewidth=1.5, alpha=0.8, label="Target: 90%")

for i, (acc, c) in enumerate(zip(accuracy, correct)):
    ax1.text(i, acc + 1, f"{acc:.0f}%\n({c}/50)", ha="center", va="bottom",
             fontsize=9, fontweight="bold", color="white")

from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor="#4a90d9", label="Kept"),
    Patch(facecolor="#d94a4a", label="Reverted"),
    plt.Line2D([0], [0], color="#ffcc00", linestyle="--", linewidth=1.5, label="Target: 90%"),
]
ax1.legend(handles=legend_elements, loc="lower right", fontsize=9,
           facecolor="#1a1d27", edgecolor="#2a2d37", labelcolor="white")
ax1.set_xticks(range(len(labels)))
ax1.set_xticklabels(labels, fontsize=8, color="#b0b8c8")
ax1.set_ylabel("Accuracy (%)", fontsize=12, color="#b0b8c8")
ax1.set_title("Classification Accuracy per Iteration", fontsize=14, fontweight="bold", color="white")
ax1.set_ylim(0, 105)
ax1.set_facecolor("#0f1117")
ax1.tick_params(colors="#b0b8c8")
for sp in ["top", "right"]:
    ax1.spines[sp].set_visible(False)
for sp in ["bottom", "left"]:
    ax1.spines[sp].set_color("#2a2d37")

# ── Chart 2: Accuracy trajectory ─────────────────────────────────────────────
ax2 = axes[0, 1]
best_so_far = []
cur_best = accuracy[0]
for i, (acc, k) in enumerate(zip(accuracy, kept)):
    if k and acc > cur_best:
        cur_best = acc
    best_so_far.append(cur_best)

ax2.plot(range(len(accuracy)), accuracy, "o-", color="#6a6d77", linewidth=1,
         markersize=6, alpha=0.5, label="Each iteration")
ax2.plot(range(len(accuracy)), best_so_far, "o-", color="#4adb8b", linewidth=2.5,
         markersize=8, label="Best so far", zorder=5)
ax2.axhline(y=90, color="#ffcc00", linestyle="--", linewidth=1.5, alpha=0.8)

ax2.annotate("REVERTED\n(CoT hurt accuracy)", xy=(3, 74), xytext=(3, 67),
             fontsize=8, color="#d94a4a", ha="center", fontweight="bold",
             arrowprops=dict(arrowstyle="->", color="#d94a4a"))
ax2.annotate(f"Target met!\n{accuracy[6]:.0f}%", xy=(6, 90), xytext=(5, 95),
             fontsize=9, color="#ffcc00", fontweight="bold",
             arrowprops=dict(arrowstyle="->", color="#ffcc00"))
ax2.annotate(f"Best: {accuracy[7]:.0f}%", xy=(7, 94), xytext=(7, 99),
             fontsize=9, color="#4adb8b", fontweight="bold",
             arrowprops=dict(arrowstyle="->", color="#4adb8b"))

ax2.set_xticks(range(len(versions)))
ax2.set_xticklabels([f"Iter {i}" for i in range(len(versions))], fontsize=9, color="#b0b8c8")
ax2.set_ylabel("Accuracy (%)", fontsize=12, color="#b0b8c8")
ax2.set_title("Optimization Trajectory", fontsize=14, fontweight="bold", color="white")
ax2.set_ylim(60, 105)
ax2.set_facecolor("#0f1117")
ax2.tick_params(colors="#b0b8c8")
ax2.legend(loc="lower right", fontsize=9, facecolor="#1a1d27", edgecolor="#2a2d37", labelcolor="white")
for sp in ["top", "right"]:
    ax2.spines[sp].set_visible(False)
for sp in ["bottom", "left"]:
    ax2.spines[sp].set_color("#2a2d37")

# ── Chart 3: Error breakdown stacked bar ─────────────────────────────────────
ax3 = axes[1, 0]
x = np.arange(len(versions))
cat_colors = ["#e74c3c", "#e67e22", "#3498db", "#1abc9c", "#9b59b6", "#95a5a6"]
bottom = np.zeros(len(versions))
for cat, color in zip(cat_names, cat_colors):
    vals = errors_data[cat]
    ax3.bar(x, vals, bottom=bottom, color=color, width=0.6, label=cat,
            edgecolor="#1a1d27", linewidth=0.5)
    bottom += np.array(vals)

ax3.set_xticks(x)
ax3.set_xticklabels([f"v{i}" for i in range(len(versions))], fontsize=10, color="#b0b8c8")
ax3.set_ylabel("Number of Errors", fontsize=12, color="#b0b8c8")
ax3.set_title("Error Breakdown by Category", fontsize=14, fontweight="bold", color="white")
ax3.set_facecolor("#0f1117")
ax3.tick_params(colors="#b0b8c8")
ax3.legend(loc="upper right", fontsize=8, facecolor="#1a1d27", edgecolor="#2a2d37",
           labelcolor="white", ncol=2)
for sp in ["top", "right"]:
    ax3.spines[sp].set_visible(False)
for sp in ["bottom", "left"]:
    ax3.spines[sp].set_color("#2a2d37")

# ── Chart 4: Remaining errors heatmap ────────────────────────────────────────
ax4 = axes[1, 1]
heatmap_data = np.array([errors_data[cat] for cat in cat_names])
im = ax4.imshow(heatmap_data, cmap="YlOrRd", aspect="auto", vmin=0, vmax=6)

ax4.set_xticks(range(len(versions)))
ax4.set_xticklabels([f"v{i}" for i in range(len(versions))], fontsize=10, color="#b0b8c8")
ax4.set_yticks(range(len(cat_names)))
ax4.set_yticklabels(cat_names, fontsize=10, color="#b0b8c8")

for i in range(len(cat_names)):
    for j in range(len(versions)):
        val = heatmap_data[i, j]
        if val > 0:
            ax4.text(j, i, str(val), ha="center", va="center",
                     fontsize=11, fontweight="bold",
                     color="white" if val >= 3 else "#333")

ax4.set_title("Error Heatmap (category x iteration)", fontsize=14, fontweight="bold", color="white")
ax4.set_facecolor("#0f1117")
ax4.tick_params(colors="#b0b8c8")
cbar = plt.colorbar(im, ax=ax4, shrink=0.8)
cbar.ax.tick_params(colors="#b0b8c8")
cbar.set_label("Errors", color="#b0b8c8")

plt.tight_layout(pad=2.0, rect=[0, 0, 1, 0.95])
out = "/Users/woojin/Desktop/02_Areas/01_Codes_automation/14_auto-research-skill/examples/prompt-optimization/results.png"
plt.savefig(out, dpi=150, facecolor="#0f1117", bbox_inches="tight")
print(f"Saved: {out}")
