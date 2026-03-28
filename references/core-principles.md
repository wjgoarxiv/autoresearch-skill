# Core Principles

Eight principles behind the autonomous research loop, derived from [Karpathy's autoresearch](https://github.com/karpathy/autoresearch) and generalized for any domain.

## The Eight Principles

| # | Principle | Definition | research.md Field |
|---|-----------|-----------|-------------------|
| 1 | **Single Metric** | Optimize exactly one measurable quantity. Multiple objectives cause the agent to game tradeoffs instead of improving. | `Success Metric` |
| 2 | **Mechanical Verification** | The metric must be computable without human judgment. If a person must evaluate, the loop cannot run autonomously. | `Success Metric → Target` |
| 3 | **Atomic Changes** | One change per iteration. Compound changes make it impossible to attribute improvement or regression to a specific modification. | Enforced by the loop protocol |
| 4 | **Keep or Revert** | If the metric improves, keep the change. Otherwise, revert immediately. No "maybe" — the decision is binary. | `History → Result` column |
| 5 | **Full History** | Record every attempt — successes AND failures. Failed approaches are as valuable as successful ones: they constrain the search space. | `History` table + `research_log.md` |
| 6 | **Constrained Search** | Explicitly define what can change and what cannot. Without boundaries, the agent may "cheat" (e.g., modifying the test set to improve accuracy). | `Search Space → Allowed / Forbidden` |
| 7 | **Autonomous Loop** | The loop runs without human intervention. Pausing for approval defeats the purpose — the agent must be trusted within its constraints. | `Constraints → pause_every: never` |
| 8 | **Relentless Persistence** | The loop runs until the budget is spent or the target is met. Stopping early is a last resort, not a default. | `Autonomy Directive` in SKILL.md |

## Why Each Principle Matters

### 1. Single Metric
- **Why:** Multi-objective optimization is NP-hard. A single metric gives the agent a clear gradient to follow.
- **Violation consequence:** The agent oscillates between objectives, improving one while regressing another. Progress stalls.
- **Example:** "Improve accuracy" (good) vs "Improve accuracy and reduce latency and increase coverage" (bad — pick one).

### 2. Mechanical Verification
- **Why:** Human-in-the-loop evaluation bottlenecks the iteration speed to human response time (~minutes). Mechanical verification enables ~12 iterations/hour.
- **Violation consequence:** The loop blocks waiting for human judgment. Overnight runs become impossible.
- **Example:** `python benchmark.py | grep median` (good) vs "Does this feel faster?" (bad).

### 3. Atomic Changes
- **Why:** If you change A and B simultaneously and the metric improves, you don't know which change helped. The agent loses its ability to learn from results.
- **Violation consequence:** Attribution confusion. The agent may keep harmful changes that were masked by a beneficial co-change.
- **Example:** "Switch from quicksort to merge sort" (good) vs "Switch to merge sort AND add caching AND change buffer size" (bad).

### 4. Keep or Revert
- **Why:** Accumulating "neutral" changes introduces complexity without benefit, and may interact negatively with future changes.
- **Violation consequence:** Codebase drift. The artifact grows in complexity without corresponding metric improvement.
- **Example:** Metric went from 2.40s to 2.38s — delta is within noise. Revert (it's not a clear improvement).

### 5. Full History
- **Why:** The history IS the agent's memory. Without it, the agent may retry failed approaches, wasting iterations.
- **Violation consequence:** Repeated failures. The agent tries the same dead end in iteration 8 that it already tried in iteration 3.
- **Format:** Both `research.md` History table (summary) and `research_log.md` (detailed reasoning).

### 6. Constrained Search
- **Why:** An unconstrained agent will find the cheapest path to improving the metric, which may be adversarial (modifying the test, lowering the bar, changing the metric definition).
- **Violation consequence:** Goodhart's Law — "When a measure becomes a target, it ceases to be a good measure."
- **Example:** `Forbidden: test_cases.json, model choice, temperature` prevents the agent from "cheating."

### 7. Autonomous Loop
- **Why:** The value of autoresearch is compounding iterations over time (overnight, over weekends). Each human interruption resets the clock.
- **Violation consequence:** The loop becomes a human-assisted tool rather than an autonomous agent. Iteration rate drops from ~12/hour to ~2/hour.
- **Exception:** `pause_every: N` is allowed for safety-critical domains, but should be the exception, not the default.

### 8. Relentless Persistence
- **Why:** The value of autoresearch compounds with iterations. 4 iterations finds local optima. 20 iterations discovers paradigm shifts. Early stopping leaves the most valuable experiments unrun.
- **Violation consequence:** The agent stops at iteration 4 with a mediocre result. The breakthrough that would have come at iteration 12 never happens.
- **Example:** Karpathy's autoresearch runs ~12 experiments/hour x 8 hours = ~100 experiments overnight. Stopping at 4 wastes 96% of the potential.

## Mapping to research.md

Every principle maps directly to a field in the `research.md` template:

| Principle | research.md Section | Enforcement |
|-----------|-------------------|-------------|
| Single Metric | `## Success Metric` | Template requires exactly one metric + direction |
| Mechanical Verification | `## Success Metric → Target` | Target must be a computable expression |
| Atomic Changes | (Loop protocol) | Agent instructed to make one change per iteration |
| Keep or Revert | `## History → Result` | Each row records KEPT or REVERTED |
| Full History | `## History` + `research_log.md` | Append-only tables and detailed logs |
| Constrained Search | `## Search Space` | Allowed and Forbidden explicitly listed |
| Autonomous Loop | `## Constraints → pause_every` | Default: `never` |
| Relentless Persistence | `Autonomy Directive` in SKILL.md | Agent instructed to never stop until budget spent or target met |
