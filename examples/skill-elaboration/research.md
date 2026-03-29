# Research: Skill Elaboration for P&ID Diagram Analysis

## Goal

Improve the existing `/pdf` skill so that an LLM can accurately extract process streams, identify equipment, and assign stream numbers from Piping and Instrumentation Diagrams (P&IDs).

**Target diagram:** Wastewater treatment plant P&ID (`wastewater-treatment-plant-pid-example.png`).

## Success Metric

Composite score combining three sub-metrics:

```
score = 0.5 * (streams_found / 15)
      + 0.3 * (streams_numbered / streams_found)
      + 0.2 * (equipment_found / 8)
```

**Target:** > 85% composite score.

## Ground Truth

| Category | Count |
|----------|-------|
| Total process streams | 15 |
| Total equipment items | 8 (Storage, Slaker, Storage Tank, Tank, Pumps x4, Future System, NPW Tank, Receiving Tank, M-box, Valve assembly, Filter/Separator, Truck) |

## Constraints

- **Max iterations:** 20
- **Evaluator:** `python evaluate.py`
- **Keep policy:** score_improvement
- `SKILL.md` must remain under 300 lines.
- All original `/pdf` skill content must be preserved (no deletions from the base skill).
- Additions must be generalizable to other P&ID diagrams, not hardcoded for this specific diagram.
- Search space is additive only: new sections may be appended, but existing sections must not be removed or rewritten.

## Search Space

| Allowed | Forbidden |
|---------|-----------|
| Add new sections after existing content | Remove or rewrite existing PDF sections |
| Add symbol definition tables | Hardcode specific equipment tag numbers |
| Add stream identification rules | Add diagram-specific coordinates |
| Add naming conventions | Exceed 300 lines |
| Add structured output templates | Break existing PDF operations |

## Iteration History

| Iter | Score | Delta | Streams | Numbered | Equipment | Status | Description |
|------|-------|-------|---------|----------|-----------|--------|-------------|
| 0 | 0.2750 | -- | -- | -- | -- | baseline | Original /pdf skill without P&ID additions |
| 1 | 0.9767 | +0.7017 | -- | -- | -- | kept | Added P&ID Analysis section with symbol ID, stream extraction, equipment ID, instrument/control loop analysis, structured output |
| 2 | 0.9767 | +0.0000 | -- | -- | -- | kept | Compacted: removed table, merged blank lines (345->330 lines) |
| 3 | 0.9767 | +0.0000 | -- | -- | -- | kept | Compacted: removed inter-section blank lines (330->316 lines) |
| 4 | 0.9767 | +0.0000 | -- | -- | -- | kept | Compacted: removed remaining blank lines between subsections (316->310 lines) |
| 5 | 0.9767 | +0.0000 | -- | -- | -- | kept | Compacted: merged step lines within subsections (310->304 lines) |
| 6 | 0.9767 | +0.0000 | -- | -- | -- | reverted | Attempted Next Steps compaction but violated additive-only constraint; reverted to v5 |
