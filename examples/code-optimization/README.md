# Example: Code Optimization

Goal: optimize `sort.py` so sorting 1,000,000 integers runs below 0.5 seconds while preserving correctness.

| Field | Value |
|---|---|
| Metric | Median runtime in seconds (`median_time_s`, minimize) |
| Evaluator | `python benchmark.py` |
| Baseline | 2.117478s |
| Best result | 0.150459s |
| Iterations logged | 8 |
| Visual result | [`results.png`](./results.png) |

## Expected Output

This example demonstrates the standard autoresearch artifact bundle:

- [`research.md`](./research.md): goal, constraints, search space, and iteration history
- [`research_log.md`](./research_log.md): detailed hypothesis/evaluation notes
- [`autoresearch-results.tsv`](./autoresearch-results.tsv): machine-readable metric trace
- [`results.png`](./results.png): visual summary of runtime improvement and best-so-far curve
- [`final_report.md`](./final_report.md): summary of the best implementation and failed alternatives

## Reproduce the Evaluator

From this directory:

```bash
python benchmark.py
```

The evaluator emits the mechanical contract used by the skill:

```json
{"pass": true, "score": -0.150459}
```

For minimize metrics, `score` is the negated metric value so higher scores are always better.
