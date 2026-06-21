# Example: Literature Review

Goal: fill evidence gaps in an exercise-timing literature review until all target categories have sufficient paper coverage.

| Field | Value |
|---|---|
| Metric | Covered categories out of 8 (`coverage_categories`, maximize) |
| Evaluator | Agent judgment with logged citations |
| Baseline | 1/8 categories |
| Best result | 8/8 categories |
| Iterations logged | 4 |
| Visual result | [`results.png`](./results.png) |

## Expected Output

- [`research.md`](./research.md): review goal, coverage metric, and category taxonomy
- [`research_log.md`](./research_log.md): search trail and papers added per iteration
- [`autoresearch-results.tsv`](./autoresearch-results.tsv): category coverage trace
- [`results.png`](./results.png): coverage progression visualization
- [`final_report.md`](./final_report.md): synthesized review with remaining caveats

This example demonstrates Tier 2-style research where the evaluator is not a local script but the loop still logs a measurable coverage metric.
