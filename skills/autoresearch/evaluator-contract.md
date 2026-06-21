# Evaluator Contract

The mechanical evaluator is an optional but recommended component for Tier 1 environments. It removes human judgment from the keep/revert decision (Principle 2: Mechanical Verification).

## Setup

In `research.md` Constraints section, add:

```
- **Evaluator:** `python evaluate.py`
- **Keep policy:** score_improvement
```

## JSON Contract

The evaluator command must print a single JSON object to stdout:

```json
{"pass": true, "score": 0.94}
```

`score` is always interpreted as **higher is better**. For metrics you minimize, emit the negated metric value as `score` (for example, RMSE `0.031` becomes `"score": -0.031`). This keeps `score_improvement` unambiguous across maximize and minimize tasks.

Evaluators may include extra fields for readability; old evaluators with only `pass` and `score` remain valid:

```json
{"pass": false, "score": -0.42, "metric_value": 0.42}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `pass` | boolean | yes | Did the experiment meet the minimum bar? |
| `score` | number | no (but recommended) | Comparison score; higher is always better |
| `metric_value` | number | no | Optional raw metric value for humans/plots; may be lower-is-better |

**Evaluator source field in TSV:** When a mechanical evaluator runs, the `evaluator_source` column in `autoresearch-results.tsv` records the command used (e.g., `python evaluate.py`). Without evaluator, it records `agent` (manual judgment).

## Execution Rules

1. Run the evaluator command via Bash, wrapped with `timeout 5m`: `timeout 5m python evaluate.py`
2. Parse stdout as JSON — find the first line that is valid JSON
3. Apply the keep policy
4. Log the evaluator output in `research_log.md`

## Error Handling

| Error | Action |
|-------|--------|
| Non-zero exit code | Treat as failed experiment — revert and continue |
| Invalid / no JSON in stdout | Treat as failed experiment — revert and continue |
| Timeout (exit code 124) | Treat as failed experiment — revert and continue |
| `pass: false` with `pass_only` policy | Revert and continue |
| `score` lower than previous best with `score_improvement` policy | Revert and continue |

## Keep Policies

**`score_improvement` (default):** Keep the experiment only if `score` strictly exceeds the previous best score. If `score` is absent from the JSON, fall back to `pass` field only. For minimize tasks, this requires `score = -metric_value` so a smaller metric produces a larger score.

**`pass_only`:** Keep any experiment where `pass` is `true`, regardless of score. Use when the metric is categorical (pass/fail) rather than continuous.

## Tier Fallback

- **Tier 1:** Evaluator runs mechanically as specified
- **Tier 2/3:** No shell access — fall back to agent's own judgment (manual evaluation). Log `evaluator_source: agent` in TSV.

## Example Evaluators

### Accuracy evaluator
```python
#!/usr/bin/env python3
import json, subprocess
result = subprocess.run(["python", "test_classifier.py"], capture_output=True, text=True)
accuracy = float(result.stdout.strip().split("accuracy:")[-1].strip())
print(json.dumps({"pass": accuracy > 0.9, "score": accuracy}))
```

### Benchmark evaluator (timing, minimize)
```python
#!/usr/bin/env python3
import json, subprocess, statistics, time
times = []
for _ in range(3):
    t0 = time.perf_counter()
    subprocess.run(["python", "sort.py"], check=True)
    times.append(time.perf_counter() - t0)
median = statistics.median(times)
print(json.dumps({"pass": median < 0.5, "score": -median, "metric_value": median}))
```

### RMSE evaluator (regression, minimize)
```python
#!/usr/bin/env python3
import json, math, csv
from predict import predict
with open("test_data.csv") as f:
    rows = list(csv.DictReader(f))
rmse = math.sqrt(sum((float(r["y"]) - predict(float(r["x"])))**2 for r in rows) / len(rows))
print(json.dumps({"pass": rmse < 0.05, "score": -rmse, "metric_value": rmse}))
```

## Notes

- The evaluator runs in the **research project directory**, not the skill directory
- Keep evaluators fast (<30s ideally, hard limit 5m via timeout)
- Evaluators must be deterministic — avoid random seeds unless averaged over multiple runs
- The evaluator must never modify files (it is a read-only measurement)
