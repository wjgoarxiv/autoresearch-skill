# Research: {Title}

## Goal
{Describe what you're trying to achieve. Be specific and measurable.}

## Success Metric
- **Metric:** {e.g., "accuracy on test set", "p95 latency", "LLM judge score 1-10"}
- **Target:** {e.g., "> 95%", "< 50ms", "> 8/10"}
- **Direction:** {maximize | minimize}

## Constraints
- **Max iterations:** 20
- **Time budget per experiment:** 5 minutes
- **Pause for review every:** never
- **Evaluator:** {optional: command that outputs JSON, e.g., `python evaluate.py`}
- **Keep policy:** score_improvement
- **Guard:** {optional: safety condition that must remain true, e.g., "all unit tests pass"}
- **Noise runs:** 1
- **Min delta:** 0
- {Add domain-specific constraints here}

## Current Approach
{Describe the current state / baseline. What exists now? What's the starting point?}

## Search Space
- **Allowed changes:** {What can the agent modify? e.g., "hyperparameters in config.yaml", "system prompt text", "algorithm in sort.py"}
- **Forbidden changes:** {What must NOT change? e.g., "test set", "API interface", "data format"}

## Context & References
{Any papers, docs, URLs, or background the agent should read first.}

---

## History
<!-- Auto-maintained by the agent. Do not edit manually. -->
| # | Change | Metric | Result | Timestamp |
|---|--------|--------|--------|-----------|
| 0 | Baseline | {initial value} | -- | {date} |
