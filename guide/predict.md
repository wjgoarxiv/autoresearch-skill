# autoresearch:predict — Multi-Perspective Deliberation Engine

## Purpose

`predict` runs a structured 8-phase deliberation protocol that forces genuine disagreement before synthesis. Inspired by structured analytic techniques (SATs) used in intelligence analysis to counter groupthink, it assigns independent personas to a question, gathers isolated positions, runs cross-examination and rebuttal rounds, detects whether consensus was reached through logic or social pressure (herd detection), and produces a neutral judge verdict with explicit confidence levels. The output is a `predict-report.md` that shows not just the conclusion but the full reasoning chain that led to it.

## When to Use

- You want a rigorous multi-perspective forecast on a consequential decision or outcome.
- You're trying to predict what will happen if a strategic, technical, or product choice is made.
- You suspect groupthink in your team's analysis and want adversarial stress-testing.
- You want devil's advocate critique applied systematically before committing to a direction.
- You need to document the deliberation behind a high-stakes recommendation.

## When NOT to Use

- You want a simple recommendation without the full deliberation overhead.
- The question has a factual, lookup-able answer (use web search, not deliberation).
- You want quick pros/cons without structured adversarial pressure.

## Usage

```
/autoresearch:predict
```

Provide your question. The agent frames it precisely, selects 4–6 personas, gathers independent positions, runs cross-examination and rebuttal, detects herd behavior, and synthesizes a verdict. All 8 phases run without interruption — you can walk away after providing the question.

**Example invocations:**
- "Predict: will our migration to microservices reduce P99 latency within 6 months?"
- "Should we launch in the EU market this quarter or wait for GDPR compliance audit?"
- "What will happen to our churn rate if we remove the free tier?"

## Output

| File | Content |
|------|---------|
| `predict-report.md` | Full report: framed question, personas, per-persona positions, cross-examination, rebuttals, anti-herd metrics, judge verdict with confidence, actionable recommendations |

## Example

**Domain:** A SaaS company deciding whether to open-source their core library.

- Framed question: "Will open-sourcing the core library increase qualified inbound leads by >20% within 12 months?"
- Personas selected: Optimist (growth marketer), Pessimist (VP Finance), Domain Expert (OSS ecosystem analyst), Devil's Advocate.
- Pre-deliberation: Optimist 80% yes, Pessimist 30% yes, Expert 55% yes, Devil's Advocate 40% yes.
- Cross-examination: Pessimist challenges Optimist's 20% estimate citing no comparable case in B2B SaaS.
- Rebuttal: Optimist cites HashiCorp data; Expert corroborates with two examples.
- Anti-herd: flip_rate = 25%, final_entropy = 0.72 — no herd warning.
- Judge verdict: 58% confidence yes. Core disagreement: whether lead quality (not quantity) increases. Key uncertainty: OSS community adoption speed.

## Tips

- For binary yes/no questions, the agent uses exactly 4 personas (Optimist, Pessimist, Expert, Contrarian) — the minimum for meaningful polarity.
- Watch the `herd_warning` field. If it triggers, the agent forces personas to re-justify independently. A herd warning on a "yes" question is often a sign the conclusion is weaker than it appears.
- The judge's "blind spots" section at the end of the report lists questions the deliberation didn't address. These are often the most valuable output — they tell you what to research next.
