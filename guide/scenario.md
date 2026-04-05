# autoresearch:scenario — 12-Dimension Scenario Explorer

## Purpose

`scenario` systematically explores a subject — a plan, design, system, or decision — across 12 dimensions and up to 5 domain modes. The 12 dimensions cover the full range from best case to adversarial to long-term drift to recovery. Domain modes (technical, business, social, regulatory, environmental) let you apply each dimension through the lens most relevant to your context. A balanced rotation loop ensures no dimension or domain is skipped or over-represented. The output is a `scenario-report.md` written incrementally, finishing with a ranked risk table and concrete recommended actions.

## When to Use

- You want to stress-test a plan or architecture before committing to it.
- You need to identify failure modes that aren't obvious from the happy path.
- You're preparing a proposal and want to anticipate objections across multiple stakeholder perspectives.
- You want a "what could go wrong" analysis that is exhaustive rather than ad-hoc.
- You're conducting scenario planning for a product launch, infrastructure change, or policy decision.

## When NOT to Use

- You want a simple pros/cons list without structured exploration.
- You want a single prediction with a confidence level (use `predict` instead).
- You just need debugging help on a specific bug.
- You want iterative metric optimization (use the main autoresearch loop).

## Usage

```
/autoresearch:scenario
```

You will be asked:
1. What is the subject of this scenario analysis? (Provide a specific system, plan, or decision.)
2. Which domain modes apply? (1) technical, (2) business, (3) social, (4) regulatory, (5) environmental — select all that apply.
3. Budget (optional): "top 6 dimensions only" or similar. Default covers all 12 × N selected modes.

After setup, the loop runs autonomously — it writes each cell to `scenario-report.md` as it completes, without waiting for all cells to finish.

## Output

| File | Content |
|------|---------|
| `scenario-report.md` | Full report: per-dimension findings organized by domain mode, summary coverage table, top-5 risks ranked by severity × likelihood, recommended actions |

## Example

**Domain:** Migrating a monolithic Django app to microservices.

- Subject: migration plan targeting Q3 cutover, 4-week timeline, 8-engineer team.
- Domain modes selected: technical, business, regulatory.
- Dimension 1 (Best case, technical): migration completes in 3 weeks, 40% latency reduction, zero data loss. Trigger: all service boundaries pre-agreed, no circular dependencies.
- Dimension 2 (Worst case, technical): data consistency failures at service boundary, 2-week rollback, customer-visible downtime.
- Dimension 5 (Cascade failure, business): delayed launch triggers contract penalty clause → team morale drop → key engineer departure → delayed recovery.
- Dimension 11 (Long-term drift, regulatory): GDPR data residency requirements conflict with the new service topology's cross-region calls — not caught until audit 18 months later.
- Key risk identified: cascade failure path from Dimension 5 has high likelihood and critical impact. Recommended action: add contractual buffer window before committing to cutover date.

## Tips

- For a 5-mode × 12-dimension run, expect a thorough report (60 cells). If you want a faster pass, specify "top 6 dimensions only" — you'll get the most asymmetric outcomes (best, worst, most likely, edge, cascade, adversarial) without the full matrix.
- Dimension 6 (Adversarial) often surfaces risks that technical reviewers miss because they aren't thinking like an attacker or a competitor.
- The "Recommended Actions" section at the end of `scenario-report.md` is derived from all cells collectively. It often contains 2–3 actions that a human reviewer would not have connected to each other.
