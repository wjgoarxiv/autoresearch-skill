# Advanced Patterns

## Guard Patterns

The `guard` field in `research.md` defines a hard safety constraint that runs after every experiment. If the guard fails, the change is reverted — regardless of metric improvement. A 50% speed improvement that breaks tests is discarded.

### Guard examples by domain

**Code optimization — correctness guard:**
```markdown
Guard: python -m pytest tests/unit/ -x -q
```
Run unit tests only (fast). The `-x` flag stops at the first failure. Use integration tests in your evaluator's secondary check, not as the guard — guards must be fast (under 30 seconds).

**ML model optimization — minimum accuracy guard:**
```markdown
Guard: python scripts/min_accuracy_check.py --threshold 0.80
```
Prevent the loop from keeping a change that achieves the speed target by tanking accuracy below an acceptable floor. The guard enforces a floor; the metric optimizes a peak.

**Web / API optimization — latency guard:**
```markdown
Guard: python scripts/latency_check.py --max-ms 200
```
Write a script that makes a test request and exits non-zero if latency exceeds the hard limit. Prevents metric improvements that sacrifice baseline responsiveness.

**Infrastructure optimization — smoke test guard:**
```markdown
Guard: bash scripts/smoke_test.sh
```
Curl a health endpoint or run a minimal end-to-end test. Prevents config changes that break the service even when the resource metric improves. Keep the smoke test to 3–5 representative calls, not a full integration suite.

### Guard design rules

1. **Fast:** run in under 30 seconds. Use a subset (fast unit tests, not the full suite).
2. **Binary:** pass or fail, no partial grades. Guards are not metrics.
3. **Specific:** guard the exact property that must never regress — not everything, just the safety-critical invariant.

Guard failures are logged as `guard_violation` in `autoresearch-results.tsv`, distinct from `revert` (metric regression) and `keep`.

---

## Noise Handling Cookbook

Benchmarks and empirical metrics vary between runs. These two fields control how the loop handles variability.

### Choosing noise_runs

| noise_runs value | Use when |
|---|---|
| `noise_runs: 1` (default) | Deterministic metrics: fixed-dataset accuracy, bundle size in KB, line counts, coverage percentage |
| `noise_runs: 3` | Moderate noise: benchmarks on a shared machine, LLM calls with temperature=0, typical ML training |
| `noise_runs: 5` | High noise: LLM judge scores, training with randomness, network latency, distributed system benchmarks |

Higher `noise_runs` multiplies evaluator cost per iteration. On a 3-minute evaluator, `noise_runs: 5` costs 15 minutes per iteration. Budget `max_iterations` accordingly.

### Choosing min_delta

`min_delta` prevents the loop from keeping changes that improve the metric by a negligible amount indistinguishable from noise.

| Metric type | Suggested min_delta | Rationale |
|---|---|---|
| Time in seconds (e.g., 1.23s) | `0.01` | Ignore sub-10ms improvements on noisy machines |
| Accuracy / F1 (0–1 range) | `0.005` | Ignore improvements under 0.5 percentage points |
| LLM judge score (1–10) | `0.1` | Judge variation of ±0.1 is within rater noise |
| RMSE on large dataset | `0.001` | Fine-grained metric warrants fine-grained threshold |
| Bundle size in KB | `1.0` | Sub-1KB improvements are not worth tracking |

### Combined example: noisy benchmark

```markdown
## Constraints
- Noise runs: 3
- Min delta: 0.01
- Guard: python -m pytest tests/ -q
```

With this setup: each evaluation runs 3 times and takes the median; a result is kept only if it beats the current best by at least 0.01; any change that breaks the test suite is reverted regardless.

---

## CI/CD Integration

Running autoresearch in CI lets you automatically optimize on a schedule or on every PR merge.

### GitHub Actions skeleton workflow

```yaml
# .github/workflows/autoresearch.yml
name: Autoresearch Optimization

on:
  schedule:
    - cron: '0 2 * * 1'   # Every Monday at 2am UTC
  workflow_dispatch:        # Manual trigger from the Actions UI

jobs:
  optimize:
    runs-on: ubuntu-latest
    timeout-minutes: 240    # 4-hour cap — CI jobs must terminate

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Verify evaluator works before starting loop
        run: python evaluate.py
        working-directory: ./research

      - name: Run autoresearch loop
        run: bash scripts/autoresearch-loop.sh ./research/
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

      - name: Upload results (always, even on partial runs)
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: autoresearch-results
          path: |
            research/research.md
            research/final_report.md
            research/progress.png
            research/autoresearch-results.tsv

      - name: Open PR if metric improved
        if: success()
        run: |
          python scripts/check_improvement.py --baseline .autoresearch-baseline
          if [ $? -eq 0 ]; then
            gh pr create --title "autoresearch: metric improved" \
              --body "$(cat research/final_report.md)"
          fi
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Key CI considerations:
- Set `timeout-minutes` — CI jobs must terminate. The loop's 5-minute-per-experiment timeout and CI's job timeout both apply.
- Upload artifacts with `if: always()` so you see results even on partial runs.
- Store evaluator output in a baseline file between CI runs to detect metric regressions across weeks.

---

## Checkpoint and Resume

The loop is crash-safe by design. Every iteration writes to disk before beginning the next. If the process dies mid-run, you lose at most one in-progress experiment.

### How the TSV and research.md enable crash recovery

At any point during the loop, completed iteration state exists in two places:

| File | What it preserves |
|---|---|
| `research.md` History table | Every completed iteration: change, metric, decision, timestamp |
| `research_log.md` | Detailed notes on every completed iteration |
| `autoresearch-results.tsv` | Machine-readable record of every completed iteration |
| `.autoresearch.lock` | Indicates a loop is currently running |

Stage 1 reads `research.md` fresh on every iteration — there is no in-memory state between iterations. This means:

1. Kill the process at any point → the last completed iteration is preserved in `research.md`
2. Restart the loop → Stage 1 reads history, sees what was tried, continues from the last logged iteration
3. Move the working directory to a different machine → the loop continues identically

### Resuming after a crash

```bash
# Check if a stale lock file exists
ls -la ./my-research/.autoresearch.lock

# If it exists and is older than 10 minutes, remove it
rm ./my-research/.autoresearch.lock

# Restart — Stage 1 reads history and picks up from where it left off
/autoresearch
```

---

## FAQ

**Q: My evaluator crashes on the first run. What do I check?**

Check three things: (1) the evaluator prints valid JSON to stdout as the last line, (2) the script exits with code 0 on success, (3) the script runs in under 5 minutes. Run `python evaluate.py` manually before starting the loop and inspect the output directly.

**Q: How many iterations should I set?**

Default 20 is a good starting point. For fast evaluators (under 10 seconds), 50 is reasonable. For slow evaluators (over 2 minutes), 10 may be enough. Rule of thumb: set `max_iterations` to at least 2× the number of distinct approaches in your search space.

**Q: The loop keeps reverting everything. Is something wrong?**

Usually one of three causes: (1) the search space is too narrow and nothing meaningfully helps, (2) the evaluator has high variance — increase `noise_runs`, (3) the baseline is already near-optimal and the target is too aggressive. Check `research_log.md` for the revert reasons — they are specific.

**Q: Can I run multiple loops on the same codebase simultaneously?**

Not recommended. Both loops modify the same files and the history tables become inconsistent. Use separate working directories for separate research threads. Each directory is fully independent.

**Q: The loop hit max_iterations without reaching the target. Did it fail?**

No. `max_iterations` is a budget, not a pass/fail threshold. The loop spent your full budget exploring the problem. Read `final_report.md` for recommendations. Common next steps: expand the search space, increase max_iterations, or reconsider whether the target is achievable under the current constraints.

**Q: Can I use this without Python? My project is TypeScript.**

Yes. The evaluator is a script you write — it can be any language. Use `evaluator: node evaluate.js` or `evaluator: npx ts-node evaluate.ts`. The loop only requires that the command outputs valid JSON to stdout and exits with code 0.

**Q: How do I stop the loop cleanly?**

Press Ctrl+C in foreground mode, or send SIGTERM to the background PID. The loop finishes the current iteration's log step before exiting. The history in `research.md` is never corrupted by a clean stop. Restart anytime — Stage 1 resumes from the last logged iteration.

**Q: I want to steer the loop toward a specific approach. Can I?**

Yes. Add it to the Search Space section of `research.md` with a note like "Priority: try this first." Stage 1 reads the search space at every iteration and will prioritize approaches you explicitly mention. You can also edit the History table between runs to add notes like "REVERT (transient OOM — retry)" to encourage the loop to revisit a promising direction.
