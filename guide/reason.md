# autoresearch:reason — Adversarial Multi-Round Reasoning

## Purpose

`reason` runs a structured multi-round debate with a blind-judge panel to reach rigorous conclusions on judgment calls where intuition or single-perspective analysis is unreliable. It assigns crypto-random IDs to all positions before critique begins — judges evaluate logic and evidence, not who proposed the argument or in what order. Positions are proposed, critiqued, rebutted, and scored across three judge dimensions (logic, evidence quality, practical applicability) until convergence or budget exhaustion. The final `verdict.md` reveals the ID-to-position mapping and explains exactly why each position won or lost.

## When to Use

- You face a decision or question where multiple genuinely defensible positions exist and you need to evaluate them fairly.
- You want the strongest arguments for and against a position surfaced and tested, not just listed.
- You want to avoid anchoring bias, framing effects, or authority bias in your reasoning process.
- You want a documented reasoning trail for a consequential architectural, product, or strategic decision.
- You want adversarial critique that will improve the argument, not just validate it.

## When NOT to Use

- You want a simple recommendation without the full multi-round structure.
- The question has a factual, lookup-able answer — `reason` is for judgment calls, not facts.
- You want a quick summary of a topic.
- You want pros/cons without adversarial pressure or judge scoring.

## Usage

```
/autoresearch:reason
```

You will be asked:
1. What is the question or decision to reason about? (Must be specific enough to allow falsifiable positions.)
2. How many positions? (Default: 3. Minimum 2, maximum 5.)
3. How many rounds? (Default: 4. Minimum 2.)

After setup, the debate runs autonomously through all rounds without stopping.

## Output

| File | Content |
|------|---------|
| `reason/rounds.md` | Per-round record: positions (by ID only), critiques, rebuttals, judge scores |
| `reason/verdict.md` | Winning argument, minority position summaries with specific logical weaknesses, synthesis, confidence level |
| `reason/id-map.md` | Revealed at end only — maps each crypto-random ID to the original position label |

## Example

**Domain:** Choosing between GraphQL and REST for a new internal API.

- Question: "For our internal microservices API with 6 teams as consumers, should we use GraphQL or REST+OpenAPI as the primary interface contract?"
- 3 positions proposed: (A) GraphQL for flexible querying, (B) REST+OpenAPI for simplicity and tooling, (C) Hybrid with REST for writes and GraphQL for reads.
- IDs assigned: ARG-7F3A (GraphQL), ARG-2C91 (REST), ARG-B44D (Hybrid).
- Round 1 critiques: ARG-2C91 challenges ARG-7F3A's assumption that all 6 teams have GraphQL expertise. ARG-7F3A challenges ARG-2C91's claim that REST avoids N+1 query problems for the reported dashboard use case.
- Round 2 rebuttals: ARG-7F3A narrows claim — GraphQL only for read-heavy consumers. ARG-B44D gains confidence after both other positions partially converge toward its boundary.
- Judge verdict: ARG-B44D wins (avg score 8.2/10). ARG-7F3A loses on practicality (team expertise gap). ARG-2C91 loses on evidence for dashboard use case.

## Tips

- The ID system is not just ceremony — it matters. Without it, judges consistently overweight the first argument or the one labeled most authoritatively. Let the IDs do their job.
- Convergence requires all judges to score the top position ≥8/10 AND no unanswered rebuttal. A position that "wins by default" because others were weak does not meet convergence — the debate continues.
- After `verdict.md` is written and `id-map.md` is revealed, read the "Synthesis" section — it captures nuances that don't fit cleanly into the winning argument and often contains the most practically useful insight.
