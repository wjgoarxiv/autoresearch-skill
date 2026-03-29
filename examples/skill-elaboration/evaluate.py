#!/usr/bin/env python3
"""Structural evaluator for P&ID skill elaboration."""
import json
import re

# Ground truth: what a good P&ID analysis skill should cover
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

def evaluate():
    try:
        with open("improved_skill/SKILL.md") as f:
            content = f.read().lower()
    except FileNotFoundError:
        print(json.dumps({"pass": False, "score": 0.0}))
        return

    # Score 1: concept coverage (0-1)
    concepts_found = sum(1 for c in REQUIRED_CONCEPTS if c in content)
    concept_score = concepts_found / len(REQUIRED_CONCEPTS)

    # Score 2: section structure (0-1) — check for relevant headings
    headings = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
    heading_text = " ".join(headings).lower()
    sections_found = sum(1 for s in REQUIRED_SECTIONS if s in heading_text)
    section_score = sections_found / len(REQUIRED_SECTIONS)

    # Score 3: depth — word count normalized (more detail = better, up to 500 words)
    word_count = len(content.split())
    depth_score = min(word_count / 500, 1.0)

    # Score 4: specific P&ID instructions (regex patterns)
    specificity_markers = [
        r"step\s*\d", r"example", r"tag\s*format", r"iso\s*\d+",
        r"arrow", r"diamond", r"circle", r"rectangle"
    ]
    specificity_found = sum(1 for m in specificity_markers if re.search(m, content))
    specificity_score = specificity_found / len(specificity_markers)

    # Composite score (weighted)
    score = round(
        0.35 * concept_score +
        0.25 * section_score +
        0.20 * depth_score +
        0.20 * specificity_score,
        4
    )

    print(json.dumps({"pass": score > 0.50, "score": score}))

if __name__ == "__main__":
    evaluate()
