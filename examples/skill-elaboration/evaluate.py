"""
Evaluation harness for skill-elaboration example.

Simulates how each iteration of the improved /pdf skill performs on
identifying streams in a P&ID diagram. Deterministic version profiles
stand in for actual skill invocations.

Ground truth: 15 streams, 8 equipment items.
"""

import json

GROUND_TRUTH = {
    "total_streams": 15,
    "total_equipment": 8,
}

# (streams_found, streams_numbered, equipment_found)
VERSION_PROFILES = {
    "v0": (4,  0,  3),
    "v1": (7,  0,  4),
    "v2": (10, 3,  6),
    "v3": (8,  2,  5),   # reverted — stuck detection L1 triggered
    "v4": (11, 7,  7),   # strategy shift after stuck detection
    "v5": (12, 10, 7),
    "v6": (13, 11, 8),   # target met (85%)
    "v7": (14, 13, 8),   # endgame mode activated
    "v8": (14, 13, 8),   # last iteration — final polish
}

REVERTED = {"v3"}


def composite_score(streams, numbered, equipment):
    """
    score = 0.5 * (streams / 15)
           + 0.3 * (numbered / max(streams, 1))
           + 0.2 * (equipment / 8)
    """
    gt = GROUND_TRUTH
    stream_ratio    = streams  / gt["total_streams"]
    numbering_ratio = numbered / max(streams, 1)
    equip_ratio     = equipment / gt["total_equipment"]
    return 0.5 * stream_ratio + 0.3 * numbering_ratio + 0.2 * equip_ratio


def evaluate_all():
    results = {}
    for version, (streams, numbered, equipment) in VERSION_PROFILES.items():
        score = composite_score(streams, numbered, equipment)
        results[version] = {
            "streams_found":    streams,
            "streams_numbered": numbered,
            "equipment_found":  equipment,
            "composite_score":  round(score, 4),
            "reverted":         version in REVERTED,
        }
    return results


def print_table(results):
    header = f"{'Version':<9} {'Streams':>8} {'Numbered':>10} {'Equipment':>11} {'Score':>8}  {'Note':<10}"
    sep    = "-" * len(header)
    print(sep)
    print(header)
    print(sep)
    for version, r in results.items():
        note = "REVERTED" if r["reverted"] else ""
        print(
            f"{version:<9} {r['streams_found']:>8}/{GROUND_TRUTH['total_streams']}"
            f" {r['streams_numbered']:>8}/{r['streams_found']:>2}"
            f" {r['equipment_found']:>9}/{GROUND_TRUTH['total_equipment']}"
            f" {r['composite_score']:>7.1%}  {note:<10}"
        )
    print(sep)

    best_kept = max(
        (r for v, r in results.items() if not r["reverted"]),
        key=lambda r: r["composite_score"],
    )
    v0_score = results["v0"]["composite_score"]
    print(f"\nBaseline (v0): {v0_score:.1%}")
    print(f"Best kept:     {best_kept['composite_score']:.1%}")
    print(f"Improvement:   +{best_kept['composite_score'] - v0_score:.1%}")


def main():
    results = evaluate_all()

    print("\n=== P&ID Skill Elaboration - Evaluation Results ===\n")
    print_table(results)

    output = {
        "ground_truth": GROUND_TRUTH,
        "results": results,
    }
    print("\n--- JSON Output ---")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
