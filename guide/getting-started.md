# Getting Started with autoresearch-skill v2.0

## 60-Second Quickstart

### Install

```bash
# Clone the skill
git clone https://github.com/wjgoarxiv/autoresearch-skill ~/.claude/plugins/autoresearch-skill

# Symlink the SKILL.md so your LLM CLI can find it
ln -s ~/.claude/plugins/autoresearch-skill/SKILL.md ~/.claude/skills/autoresearch.md

# Verify the install — ask the agent to read the skill file
cat ~/.claude/skills/autoresearch.md | head -5
```

**Requirements:** Python 3.8+ standard library only. No pip installs needed.

### Three Commands to Start

```bash
# 1. Plan your research (interactive wizard — takes ~2 minutes)
/autoresearch:plan

# 2. Run the optimization loop
/autoresearch

# 3. Ship the result when done
/autoresearch:ship
```

That is the full pipeline. Everything else is optional depth.

---

## How to Pick Your First Command

| I want to... | Command | What it does |
|---|---|---|
| Set up a new research project from scratch | `/autoresearch:plan` | 7-step wizard → writes `research.md` |
| Run the optimization loop (research.md exists) | `/autoresearch` | 5-stage loop until target met or budget spent |
| Investigate why something is broken | `/autoresearch:debug` | Scientific hypothesis → falsification loop |
| Fix a list of errors automatically | `/autoresearch:fix` | Cascade-aware error crusher, stops at 0 errors |
| Predict outcomes before committing | `/autoresearch:predict` | Multi-persona deliberation, anti-herd detection |
| Audit for security vulnerabilities | `/autoresearch:security` | STRIDE + OWASP iterative audit |
| Explore edge cases and scenarios | `/autoresearch:scenario` | 12-dimension scenario exploration |
| Reason carefully before acting | `/autoresearch:reason` | Adversarial refinement with blind-judge panel |
| Deploy or publish a finished artifact | `/autoresearch:ship` | 8-phase pipeline, one mandatory confirm gate |

---

## Metric Cheat Sheet: 15 Domains

When `/autoresearch:plan` asks for a metric in step 2, use this table to pick the right one.

| Domain | Metric name | Direction | Quick evaluator snippet |
|---|---|---|---|
| Code performance | `median_time_s` | minimize | `timeit` 3 runs, take median |
| ML accuracy | `accuracy` | maximize | `sklearn.metrics.accuracy_score(y_test, y_pred)` |
| Bundle size | `bundle_kb` | minimize | `du -sk dist/ \| cut -f1` |
| Prompt quality | `llm_judge_score` | maximize | GPT-4o rates output 1–10, average over 5 prompts |
| Literature coverage | `papers_found` | maximize | Count matched papers against target list |
| API latency | `p95_ms` | minimize | 100 requests, 95th percentile |
| Memory usage | `peak_mb` | minimize | `/usr/bin/time -v` → Maximum resident set size |
| Test coverage | `coverage_pct` | maximize | `coverage run -m pytest && coverage report` |
| RMSE | `rmse` | minimize | `sqrt(mean_squared_error(y_true, y_pred))` |
| Security coverage | `coverage_pct` | maximize | Fixed findings / total identified findings |
| Compression ratio | `ratio` | maximize | `original_bytes / compressed_bytes` |
| Translation BLEU | `bleu_score` | maximize | `sacrebleu` against reference translations |
| Database query | `query_ms` | minimize | `EXPLAIN ANALYZE` → `Execution Time:` field |
| LLM judge score | `score_1_10` | maximize | Blind 1–10 rating averaged across N=5 samples |
| Simulation RMSD | `rmsd` | minimize | RMSD between simulated and reference coordinates |

**Tips:**
- If your metric varies between runs (benchmarks, LLM calls), set `noise_runs: 3` in research.md.
- Use the `guard` field to protect correctness requirements while optimizing the primary metric.
- A metric name like `median_time_s` is better than `time` — be specific and include units.

---

## My First Research.md: Sort Optimization Walkthrough

This walks through the canonical sort optimization example from `examples/code-optimization/`. The goal is to reduce execution time of a Python sort function to under 0.5 seconds on 1 million integers.

### Step 1: Run the plan wizard

```
/autoresearch:plan
```

Answer the wizard questions:

- **Goal:** "Reduce sort.py execution time to under 0.5s on 1M integers"
- **Metric:** `median_time_s`, direction: minimize, target: `< 0.5`
- **Noisy?** Yes — benchmarks vary. Set `noise_runs: 3`
- **Search space:** Allowed: `sort.py` algorithm only. Forbidden: function signature, test files.
- **Guard:** `python -m pytest test_sort.py`
- **Max iterations:** 20
- **Evaluator:** Yes — the wizard writes `benchmark.py` for you

The wizard generates `benchmark.py`:

```python
#!/usr/bin/env python3
import json, subprocess, statistics, time

TARGET = 0.5
N_RUNS = 3

times = []
for _ in range(N_RUNS):
    t0 = time.perf_counter()
    subprocess.run(["python", "sort.py"], check=True)
    times.append(time.perf_counter() - t0)

median = statistics.median(times)
print(json.dumps({"pass": median < TARGET, "score": round(median, 4)}))
```

The wizard runs `python benchmark.py` once to record your baseline:

```json
{"pass": false, "score": 2.3991}
```

Baseline confirmed: `median_time_s = 2.3991`. Target: `< 0.5`.

The wizard writes `research.md`:

```markdown
# Research: Sort Optimization

## Goal
Reduce sort.py execution time to under 0.5s on 1M integers.

## Success Metric
- Metric: median_time_s
- Target: < 0.5
- Direction: minimize

## Constraints
- Max iterations: 20
- Evaluator: python benchmark.py
- Keep policy: score_improvement
- Guard: python -m pytest test_sort.py
- Noise runs: 3
- Min delta: 0

## History
| # | Change | Metric | Result | Timestamp |
|---|--------|--------|--------|-----------|
| 0 | Baseline (recursive quicksort) | 2.3991 | -- | 2026-04-05 |
```

### Step 2: Run the loop

```
/autoresearch
```

The agent runs the 5-stage loop repeatedly. A sample of what happens:

- **Iteration 1:** Hypothesis: "Radix sort (LSD, base 256) should be faster." → 0.8709s → KEEP
- **Iteration 2:** Hypothesis: "Base 65536 reduces passes from 4 to 2." → 0.5727s → KEEP
- **Iteration 3:** Micro-optimized radix with unrolled passes → 0.4979s → KEEP (target met)

The loop writes `progress.png` after each iteration — a convergence plot showing metric vs iteration number. Open it anytime to see progress.

### Step 3: Ship when done

```
/autoresearch:ship
```

The 8-phase shipping pipeline runs tests, checks for security issues, verifies documentation, and asks for one confirmation before any irreversible action.

### What you get at the end

| File | Contents |
|---|---|
| `research.md` | Full history of every iteration with metric values |
| `research_log.md` | Detailed notes on each experiment (hypothesis, output, decision) |
| `progress.png` | Convergence plot: metric vs iteration |
| `autoresearch-results.tsv` | Machine-readable results table (8 columns) |
| `final_report.md` | Summary with best result and recommendations for next steps |
