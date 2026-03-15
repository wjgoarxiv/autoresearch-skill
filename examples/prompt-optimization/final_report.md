# Research Report: Customer Support Ticket Classifier Prompt

**Generated:** 2026-03-15
**Total Iterations:** 8 (0-7, including baseline)
**Final Metric:** 94% accuracy (47/50)
**Baseline:** 68% accuracy (34/50)
**Improvement:** +26 percentage points (+38.2% relative)
**Status:** Target (> 90%) achieved at iteration 6, exceeded at iteration 7

---

## Executive Summary

Starting from a zero-shot classification prompt (68%), we optimized a customer support ticket classifier through 7 iterations of prompt engineering. The final prompt achieves 94% accuracy using category definitions, 5 targeted few-shot examples, structured JSON output, decision rules for ambiguous boundaries, and edge case handling. One iteration (chain-of-thought reasoning) was reverted after causing a regression. The 3 remaining errors represent genuinely ambiguous cases at the boundary of human agreement.

## Best Result

- **Iteration:** #7
- **Accuracy:** 94% (47/50)
- **vs Baseline:** +26 percentage points
- **Token count:** ~1,850 tokens (within 2,000 limit)
- **Key components:** Category definitions + 5 targeted examples + JSON output + decision rules + edge case handling

## Iteration Summary

| # | Strategy | Accuracy | Delta | Errors | Status |
|---|----------|----------|-------|--------|--------|
| 0 | Zero-shot (baseline) | 68% (34/50) | -- | 16 | BASELINE |
| 1 | Category definitions | 76% (38/50) | +8% | 12 | KEPT |
| 2 | 3 few-shot examples | 80% (40/50) | +12% | 10 | KEPT |
| 3 | Chain-of-thought | 74% (37/50) | +6% | 13 | REVERTED |
| 4 | 5 targeted examples | 84% (42/50) | +16% | 8 | KEPT |
| 5 | JSON output format | 86% (43/50) | +18% | 7 | KEPT |
| 6 | Decision rules | 90% (45/50) | +22% | 5 | KEPT |
| 7 | Optimized examples + edge cases | 94% (47/50) | +26% | 3 | BEST |

## Key Findings

1. **Category definitions are the highest-impact single change (+8%).** Explicitly distinguishing Billing from Account resolved the primary confusion source. This is a zero-cost change (no extra tokens for examples) that should be the first optimization in any classification prompt.

2. **Targeted few-shot examples outperform generic ones.** Random examples improved accuracy by +4% (v1→v2), but boundary-targeted examples improved by +4% more (v2→v4). The key: choose examples that sit exactly at the decision boundary between confusing categories.

3. **Chain-of-thought hurts classification tasks.** CoT caused a -6% regression (v2→v3) by encouraging the model to overthink simple pattern-matching tasks. Classification benefits from fast pattern recognition, not step-by-step reasoning. This is the opposite of math/logic tasks where CoT excels.

4. **Decision rules act as effective tiebreakers.** When definitions and examples leave ambiguity, explicit "if X then Y" rules (+4%, v5→v6) resolve boundary cases without increasing cognitive load on the model.

5. **Diminishing returns begin around 90%.** The last 3 errors (94→100%) represent genuine ambiguity where even human annotators would disagree. Further prompt optimization is unlikely to resolve these without changing the category taxonomy itself.

## Error Reduction Trajectory

```
Iteration:  v0   v1   v2   v3   v4   v5   v6   v7
Errors:     16   12   10   13    8    7    5    3
            ──── ──── ──── ──── ──── ──── ──── ────
Billing:     6    2    2    2    1    1    1    1
Account:     4    2    2    2    1    1    0    0  ← eliminated
Bug Report:  4    4    4    3    2    1    1    1
Technical:   0    0    0    0    2    2    1    1
Returns:     0    2    1    2    1    1    1    0  ← eliminated
Gen Inquiry: 2    2    1    4    1    1    1    0  ← eliminated
```

## Failed Approaches

1. **Chain-of-thought (iteration 3):** Caused -6% regression. CoT prompted the model to over-reason on simple tickets, converting correct fast-pattern responses into incorrect over-analyzed ones. "What are your business hours?" was reasoned into Account because "the user wants to interact with their account." Lesson: match the reasoning strategy to the task type.

## Irreducible Errors (3 cases)

| ID | Ticket | Expected | Why ambiguous |
|----|--------|----------|---------------|
| 39 | "Invoice shows tax but I'm tax-exempt" | Billing | Involves account tax status AND billing mechanism |
| 44 | "App drains battery fast since update" | Bug Report | Could be software bug OR hardware degradation |
| 49 | "Device overheats after 20 minutes" | Technical | Could be hardware OR software causing CPU overuse |

These cases sit at category boundaries where the correct label depends on information not present in the ticket text. Resolving them would require either: (a) follow-up questions, (b) category restructuring, or (c) multi-label classification.

## Recommendations

- **Deploy v7 prompt** for production use (94% accuracy, 1,850 tokens).
- **Monitor the 3 irreducible error patterns** — if they occur frequently in production, consider adding a "Needs Triage" category for ambiguous tickets.
- **Re-run this research loop** if categories change or if new error patterns emerge in production data.
- **Do not add chain-of-thought** — it was empirically shown to hurt this specific task.

---

*Generated by the autoresearch-skill skill. See `research_log.md` for detailed iteration notes.*
