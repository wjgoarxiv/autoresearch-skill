# Example: Function Fitting

Goal: discover an unknown function from `train_data.csv` and minimize RMSE on held-out `test_data.csv`.

| Field | Value |
|---|---|
| Metric | RMSE (`rmse`, minimize) |
| Evaluator | `python evaluate.py` |
| Baseline | 2.113831 RMSE |
| Best result | 0.030197 RMSE |
| Iterations logged | 8 |
| Visual result | [`results.png`](./results.png) |

## Expected Output

- [`research.md`](./research.md): loop configuration and history
- [`research_log.md`](./research_log.md): experiment notes and pivot trail
- [`autoresearch-results.tsv`](./autoresearch-results.tsv): RMSE trace by iteration
- [`results.png`](./results.png): convergence plot plus fitted curve visualization
- [`final_report.md`](./final_report.md): final model summary and reproducibility notes

## Reproduce the Evaluator

From this directory:

```bash
python evaluate.py
```

The evaluator prints JSON such as:

```json
{"pass": true, "score": -0.030197}
```

For minimize metrics, `score` is the negated metric value so higher scores are always better.
