# /autoresearch — Core Loop Reference

The core autonomous research loop. Reads `research.md`, proposes hypotheses, runs experiments, keeps improvements, discards failures, and iterates until the target metric is achieved or the iteration budget is spent.

---

## Command Reference

```bash
# Basic invocation (research.md in current directory)
/autoresearch

# Explicit path
/autoresearch ./my-research/research.md

# Overnight — foreground, runs in your terminal
bash scripts/autoresearch-loop.sh ./my-research/

# Overnight — background, survives terminal close
nohup bash scripts/autoresearch-loop.sh ./my-research/ > autoresearch.log 2>&1 &

# Check progress of a running loop
bash scripts/check_progress.sh ./my-research/
```

---

## Pre-Flight Questions

Before the loop starts, the agent asks two setup questions if they are not already answered in `research.md`. Do not skip these — they determine how the loop runs.

### Question 1: Overnight or paused?

> "Do you want this research loop to run unattended (overnight)?"

| Answer | Effect |
|---|---|
| **Yes** | Sets `pause_every: never`. Agent runs to completion without stopping. Recommends nohup or tmux. |
| **No** | Asks: "How often should I pause for your review?" Sets `pause_every: N` iterations. |

Recommendation for most users: say yes. The loop is designed for unattended operation. Pausing is only useful for safety-critical domains (e.g., production infrastructure) where human review before each batch is required.

If `research.md` already has `pause_every` set, this question is skipped.

### Question 2: Do you have an evaluator?

> "Do you have a script that can automatically measure the success metric?"

| Answer | Effect |
|---|---|
| **Yes** | Records the evaluator command (e.g., `python evaluate.py`). Asks keep policy: `score_improvement` or `pass_only`. |
| **No** | Agent judges manually using available tools. Slower and less consistent — consider adding a script for runs of more than 5 iterations. |

An evaluator is any script that outputs `{"pass": bool, "score": number}` to stdout. See the Evaluator Design section below.

---

## The 5 Stages in Plain English

```
[research.md]
     |
     v
[Stage 1: Understand] --> [Stage 2: Hypothesize] --> [Stage 3: Experiment]
                                                              |
                                          [Stage 5: Log] <-- [Stage 4: Evaluate]
                                               |
                                    (loop back to Stage 1)
```

### Stage 1 — Understand

The agent reads `research.md` from top to bottom and loads everything it needs to make a good next decision: the goal, the success metric, all constraints, and the full history of what has been tried. It assesses the gap between the current best result and the target, and checks whether a stuck-detection pivot is needed.

What happens: reads goal, metric, constraints, history. Identifies patterns in what worked and what failed.

### Stage 2 — Hypothesize

The agent proposes exactly one specific, testable change. The hypothesis follows the format: "Changing X to Y should improve the metric because Z." It avoids repeating approaches that have already failed.

What happens: one concrete hypothesis is proposed and logged before any code is touched.

### Stage 3 — Experiment

The agent executes the change. All Bash commands are wrapped with `timeout 5m` to enforce the 5-minute per-experiment budget. If the timeout fires (exit code 124), the experiment is treated as failed — the change is reverted and the iteration is logged as `TIMEOUT`.

What happens: code is modified or commands are run. If it crashes or times out, the change is reverted before proceeding.

### Stage 4 — Evaluate

The agent runs the evaluator and parses the JSON result. It compares the new score against the current best, applies the keep policy and `min_delta` threshold, and checks the guard condition if one is defined. If `noise_runs > 1`, it runs the evaluator multiple times and takes the median.

What happens: evaluator runs, result is compared to current best, keep or revert decision is made.

### Stage 5 — Log and Iterate

The agent updates all output files, then checks the two termination conditions. If neither is met, it immediately begins Stage 1 of the next iteration — no pause, no summary, no prompt.

What happens: four files are updated. Then: target met? Done. Budget spent? Done. Otherwise, back to Stage 1 NOW.

---

## Evaluator Design

### When to write one

Write an evaluator when:
- The metric is a number a script can compute (timing, accuracy, size, score)
- You will run more than 5 iterations (manual evaluation at scale is unreliable)
- You need reproducible, objective comparisons between iterations

Skip the evaluator when:
- The metric requires human judgment with no proxy (e.g., aesthetic quality)
- You are doing a one-shot experiment
- The evaluation takes more than 4 minutes (leave 1 minute buffer for the 5-minute timeout)

### The {"pass": bool, "score": number} contract

Every evaluator must print exactly one JSON line to stdout:

```json
{"pass": true, "score": 0.94}
```

- `pass` (bool): did this iteration meet the threshold?
- `score` (number): the raw metric value — lower is better if direction is minimize, higher if maximize

The agent reads the last valid JSON line from stdout. Other output (print statements, progress logs) is allowed but the JSON line must be present and valid.

### Example Evaluator 1: Benchmark timing (minimize)

```python
#!/usr/bin/env python3
"""Evaluator: median execution time over 3 runs. Target: < 0.5s."""
import json, subprocess, statistics, time

TARGET = 0.5
N_RUNS = 3

times = []
for _ in range(N_RUNS):
    t0 = time.perf_counter()
    result = subprocess.run(["python", "sort.py"], capture_output=True)
    if result.returncode != 0:
        print(json.dumps({"pass": False, "score": 999.0}))
        raise SystemExit(1)
    times.append(time.perf_counter() - t0)

median = statistics.median(times)
print(json.dumps({"pass": median < TARGET, "score": round(median, 4)}))
```

### Example Evaluator 2: RMSE on test set (minimize)

```python
#!/usr/bin/env python3
"""Evaluator: RMSE on held-out test set. Target: < 0.05."""
import json, subprocess

TARGET = 0.05

result = subprocess.run(
    ["python", "predict.py", "--test-only"],
    capture_output=True, text=True
)
# Expects last line of stdout: "rmse: 0.0312"
last_line = result.stdout.strip().split("\n")[-1]
rmse = float(last_line.split(":")[-1].strip())
print(json.dumps({"pass": rmse < TARGET, "score": round(rmse, 6)}))
```

---

## Overnight Modes

### Foreground — runs in your terminal, Ctrl+C to stop

```bash
bash scripts/autoresearch-loop.sh ./my-research/
```

Use when: you want to watch progress in real time and can keep the terminal open.

### nohup — background, survives terminal close

```bash
nohup bash scripts/autoresearch-loop.sh ./my-research/ > autoresearch.log 2>&1 &
echo "PID: $!"   # save this to kill later if needed
```

Use when: you want to close the terminal and check in the morning. No tmux required.

### tmux — background, reattachable

```bash
tmux new-session -d -s research 'bash scripts/autoresearch-loop.sh ./my-research/'
tmux attach -t research    # reattach anytime to watch live output
tmux kill-session -t research  # stop the loop
```

Use when: you want to be able to reattach and watch live output from any terminal.

### Monitoring progress

```bash
bash scripts/check_progress.sh ./my-research/
```

Sample output:
```
Research: Sort Optimization
Iteration: 12/20
Best so far: 0.4979 (iteration 3) — target: < 0.5 [ACHIEVED]
Last 3 iterations: KEEP, REVERT, REVERT
Status: converging
Last updated: 2026-04-05 03:41
```

---

## Guard, noise_runs, and min_delta

These three fields in `research.md` Constraints control safety and statistical rigor.

| Field | Purpose | When to use |
|---|---|---|
| `guard` | Hard constraint — revert if it fails, regardless of metric | Any time you have a correctness requirement that must never regress |
| `noise_runs` | Run evaluator N times, take median | Any metric that varies between runs (benchmarks, LLM calls, network latency) |
| `min_delta` | Require at least this much improvement to count as "better" | Noisy metrics where tiny improvements may be noise, not signal |

### guard

```markdown
Guard: python -m pytest tests/unit/ -x -q
```

Runs after every experiment. If it fails, the change is reverted regardless of metric improvement. A 50% metric improvement that breaks tests is discarded. Guard failures are logged as `guard_violation` in the TSV, not as `revert`.

### noise_runs

| Value | Use when |
|---|---|
| `noise_runs: 1` (default) | Deterministic metrics: fixed-dataset accuracy, bundle size, line count |
| `noise_runs: 3` | Moderate noise: benchmarks on a shared machine, typical ML training |
| `noise_runs: 5` | High noise: LLM judge scores, training with randomness, network latency |

Higher `noise_runs` costs more time per iteration. On a 3-minute evaluator, `noise_runs: 5` costs 15 minutes per iteration. Budget accordingly.

### min_delta

| Metric type | Suggested value | Rationale |
|---|---|---|
| Time in seconds | `0.01` | Ignore sub-10ms improvements on noisy machines |
| Accuracy / F1 (0–1) | `0.005` | Ignore improvements under 0.5 percentage points |
| LLM judge score (1–10) | `0.1` | Judge variation of ±0.1 is within rater noise |
| RMSE | `0.001` | Fine-grained metric warrants fine-grained threshold |

---

## Stuck Detection: Level 1, 2, and 3

The loop never stops when stuck. It pivots strategy and continues spending the iteration budget.

### Level 1: 3 consecutive non-improving iterations

**Trigger:** 3 iterations in a row with no improvement (revert or no change).

**Response:** Switch to a different strategy within the current approach. If the loop has been trying algorithmic variants, switch to memory layout or compiler flags.

```
[PIVOT L1] 3 consecutive non-improving iterations
  Previous strategy: algorithmic variants
  Switching to: memory layout and cache optimization
  Continuing iteration 8...
```

### Level 2: 5 consecutive non-improving iterations

**Trigger:** 5 iterations in a row with no improvement.

**Response:** Paradigm shift — abandon the current approach entirely and try something fundamentally different.

```
[PIVOT L2] 5 consecutive non-improving iterations
  Previous paradigm: pure Python optimization
  Switching to: Cython / C extension paradigm
  Continuing iteration 11...
```

### Level 3: max_iterations reached

**Trigger:** The iteration budget is exhausted.

**Response:** Normal termination. The loop writes `final_report.md` with the best result, the full search path, and recommendations for further work. This is not failure — it means you spent the full budget.
