# autoresearch:debug — Scientific Bug Investigation

## Purpose

`debug` is a systematic root-cause analysis engine based on the scientific method. Instead of guessing at causes or making ad-hoc code changes, it forces you to form falsifiable hypotheses, design tests that could disprove each one, run them, and log everything. The result is a `debug/` folder with three structured files: active hypotheses, eliminated candidates (with proof), and confirmed findings. The key discipline is that a hypothesis is only accepted as root cause after a positive confirmation test — not just because it "survived" other tests.

## When to Use

- You have a bug whose root cause is genuinely unclear and you need to investigate systematically.
- You want a full investigation trail (for post-mortems, team handoffs, or future reference).
- The bug is intermittent or hard to reproduce and you need to eliminate candidates methodically.
- You want to apply structured analytic techniques (binary search, differential diagnosis, instrumentation) rather than random probing.
- Someone asks "why is this failing?" and the answer is not obvious.

## When NOT to Use

- The bug's root cause is already known — use `fix` to eliminate it iteratively.
- You want to optimize a metric, not fix a defect — use the main `autoresearch` loop.
- You just need a quick one-line explanation of what a function does.

## Usage

```
/autoresearch:debug
```

You will be asked three questions at setup:

1. What is the bug? (Paste the error message or describe the failing behavior.)
2. What is the last known good state? (Last commit that worked, last config that worked.)
3. How many investigation iterations before stopping? (Default: 15.)

After setup, the investigation is fully autonomous. The agent forms hypotheses, runs tests, logs results, and begins the next iteration without pausing.

## Output

| File | Content |
|------|---------|
| `debug/hypotheses.md` | Active candidates, sorted by confidence (high first), each with a falsifying test defined |
| `debug/eliminated.md` | Ruled-out hypotheses with proof of elimination (exact test result that disproved each) |
| `debug/findings.md` | Symptom summary, per-iteration log, and final confirmed root cause with reproduction case |

## Example

**Domain:** A FastAPI service returns 503 intermittently under load.

- Symptom: `503 Service Unavailable` appears on ~5% of requests above 100 req/s.
- Hypotheses formed: H-1 (connection pool exhausted), H-2 (slow DNS on upstream call), H-3 (thread pool saturation).
- H-1 test: log active connections during failure window. Result: count = 8/50 — pool not exhausted. H-1 eliminated.
- H-2 test: replace hostname with IP in upstream URL. 503s disappear. H-2 confirmed.
- Root cause: DNS resolution latency spikes under load, causing upstream timeout before the 500ms limit.
- Proposed fix: cache DNS resolution or use IP-based upstream config.

## Tips

- If 3 iterations pass without eliminating any hypothesis, the agent will automatically switch technique (e.g., from log analysis to binary bisect). You do not need to prompt this.
- The `debug/eliminated.md` file is often more valuable than `findings.md` — it shows what the bug is NOT, which narrows the search space for future contributors.
- After `debug` confirms a root cause, the natural next step is `/autoresearch:fix` — the findings file tells you exactly what to change.
