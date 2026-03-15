"""
Prompt optimization evaluation harness.

Simulates how different prompt engineering strategies affect classification
accuracy on the 50-case test set. Each prompt version has a deterministic
accuracy profile based on which failure modes it addresses.

This is a SIMULATION for the autoresearch-skill example. In a real scenario,
each iteration would call an actual LLM API.
"""

import json
import sys
from pathlib import Path

# Load test cases
TEST_CASES = json.loads(Path(__file__).with_name("test_cases.json").read_text())

# ── Failure profiles per prompt version ──────────────────────────────────────
# Each version lists the test case IDs it gets WRONG.
# Designed to realistically model how each prompt change fixes specific errors.

FAILURE_PROFILES = {
    "v0": {
        # Zero-shot: 68% (34/50). Billing/Account confusion, vague Bug Reports,
        # General Inquiry over-classification
        "wrong": [9, 23, 31, 39, 45, 50,   # Billing confused with Account (6)
                  11, 25, 33, 47,            # Account confused with Billing (4)
                  10, 15, 29, 44,            # Bug Reports missed (symptoms, not tech terms) (4)
                  43, 38,                    # General Inquiry misclassified (2)
                  ],
        "desc": "Baseline: zero-shot prompt with category list only",
    },
    "v1": {
        # Add category definitions: 76% (38/50). Fixes most Billing/Account confusion
        "wrong": [39, 50,                   # Billing edge cases remain (2)
                  33, 47,                    # Account edge cases remain (2)
                  10, 15, 29, 44,            # Bug Reports still missed (4)
                  43, 38,                    # General Inquiry still misclassified (2)
                  35, 20,                    # Returns with vague wording (2)
                  ],
        "desc": "Added explicit category definitions (Billing vs Account distinction)",
    },
    "v2": {
        # Add 3 few-shot examples: 80% (40/50). Fixes some Bug Reports
        "wrong": [39, 50,                   # Billing edge cases (2)
                  33, 47,                    # Account edge cases (2)
                  44, 29,                    # Bug Reports (subtle symptoms) (2)
                  43,                        # General Inquiry (1)
                  35,                        # Returns edge case (1)
                  46, 37,                    # Bug Reports (UI-related, not obvious) (2)
                  ],
        "desc": "Added 3 few-shot examples (Billing, Bug Report, Account)",
    },
    "v3": {
        # Chain-of-thought: 74% (37/50). REGRESSION -- CoT causes overthinking
        "wrong": [39, 50,                   # Billing edge cases (2)
                  33, 47,                    # Account edge cases (2)
                  44, 29, 46,               # Bug Reports (3)
                  43, 38, 30, 16,           # General Inquiry over-expanded (4)
                  35, 20,                    # Returns (2)
                  ],
        "desc": "Added chain-of-thought reasoning step",
    },
    "v4": {
        # 5 few-shot examples (targeted): 84% (42/50). Back on track
        "wrong": [39,                        # Billing edge case (1)
                  47,                        # Account edge case (1)
                  44, 46,                    # Bug Reports (subtle) (2)
                  43,                        # General Inquiry (1)
                  35,                        # Returns edge case (1)
                  49, 40,                    # Technical (ambiguous symptoms) (2)
                  ],
        "desc": "5 targeted few-shot examples (one per confusing category pair)",
    },
    "v5": {
        # Structured JSON output: 86% (43/50). Format enforcement reduces noise
        "wrong": [39,                        # Billing edge case (1)
                  47,                        # Account edge case (1)
                  44,                        # Bug Report (battery drain) (1)
                  43,                        # General Inquiry (1)
                  35,                        # Returns edge case (1)
                  49,                        # Technical (ambiguous) (1)
                  40,                        # Technical (quality issue) (1)
                  ],
        "desc": "Added structured JSON output format with confidence field",
    },
    "v6": {
        # Decision rules for ambiguous cases: 90% (45/50). TARGET MET
        "wrong": [39,                        # Billing (tax-exempt invoice) (1)
                  44,                        # Bug Report (battery = Technical?) (1)
                  43,                        # General Inquiry (user manual) (1)
                  49,                        # Technical (overheating) (1)
                  35,                        # Returns (description mismatch) (1)
                  ],
        "desc": "Added explicit decision rules for Billing/Account and Bug/Technical boundaries",
    },
    "v7": {
        # Optimized examples + edge case instructions: 94% (47/50). BEST
        "wrong": [39,                        # Billing (tax-exempt -- very ambiguous) (1)
                  44,                        # Bug Report (battery drain -- hardware or software?) (1)
                  49,                        # Technical (overheating -- hardware issue) (1)
                  ],
        "desc": "Optimized example selection + added edge case handling instructions",
    },
}


def evaluate_version(version: str) -> dict:
    """Evaluate a prompt version against the test set."""
    profile = FAILURE_PROFILES[version]
    wrong_ids = set(profile["wrong"])
    total = len(TEST_CASES)

    results = []
    for tc in TEST_CASES:
        correct = tc["id"] not in wrong_ids
        results.append({
            "id": tc["id"],
            "text": tc["text"][:60] + "..." if len(tc["text"]) > 60 else tc["text"],
            "expected": tc["category"],
            "correct": correct,
        })

    n_correct = sum(1 for r in results if r["correct"])
    accuracy = n_correct / total

    # Collect errors by category
    errors_by_cat = {}
    for r in results:
        if not r["correct"]:
            cat = r["expected"]
            errors_by_cat[cat] = errors_by_cat.get(cat, 0) + 1

    return {
        "version": version,
        "desc": profile["desc"],
        "correct": n_correct,
        "total": total,
        "accuracy": round(accuracy, 4),
        "accuracy_pct": round(accuracy * 100, 1),
        "errors_by_category": errors_by_cat,
        "wrong_ids": sorted(wrong_ids),
    }


def main():
    print("=" * 65)
    print("Prompt Optimization — Auto-Research Evaluation Harness")
    print("=" * 65)
    print(f"Test set: {len(TEST_CASES)} cases, 8 categories\n")

    all_results = []
    baseline_acc = None

    for version in sorted(FAILURE_PROFILES.keys()):
        r = evaluate_version(version)
        all_results.append(r)

        if version == "v0":
            baseline_acc = r["accuracy_pct"]

        delta = r["accuracy_pct"] - baseline_acc
        kept = "REVERTED" if version == "v3" else ("KEPT" if delta >= 0 else "REVERTED")

        print(f"{'='*65}")
        print(f"  {version}: {r['desc']}")
        print(f"  Accuracy: {r['accuracy_pct']}% ({r['correct']}/{r['total']})")
        print(f"  vs Baseline: {delta:+.1f}%  |  {kept}")
        if r["errors_by_category"]:
            errs = ", ".join(f"{k}: {v}" for k, v in sorted(r["errors_by_category"].items()))
            print(f"  Errors: {errs}")
        print()

    # Summary table
    print("=" * 65)
    print("SUMMARY")
    print("=" * 65)
    print(f"{'Ver':<5} {'Acc':>6} {'Correct':>8} {'Delta':>8} {'Status':<10} {'Description'}")
    print(f"{'-'*5} {'-'*6} {'-'*8} {'-'*8} {'-'*10} {'-'*40}")
    best_acc = baseline_acc
    for r in all_results:
        delta = r["accuracy_pct"] - baseline_acc
        if r["version"] == "v3":
            status = "REVERTED"
        elif r["version"] == "v0":
            status = "BASELINE"
        elif r["accuracy_pct"] > best_acc:
            best_acc = r["accuracy_pct"]
            status = "KEPT"
        else:
            status = "KEPT"
        print(f"{r['version']:<5} {r['accuracy_pct']:>5.1f}% {r['correct']:>4}/{r['total']:<3} {delta:>+7.1f}% {status:<10} {r['desc'][:45]}")

    # JSON for programmatic use
    print(f"\n__RESULTS_JSON__:{json.dumps(all_results, default=str)}")


if __name__ == "__main__":
    main()
