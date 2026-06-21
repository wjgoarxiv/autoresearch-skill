# autoresearch:learn

`/autoresearch:learn` converts feedback about the skill itself into a small improvement package: a failure taxonomy entry, a proposed patch plan, and an eval scenario that would catch the failure in the future.

Use it when:

- A run stopped too early or ignored the iteration budget
- An evaluator contract was confusing or misapplied
- Install docs did not match your platform
- The final artifacts were unclear
- A web page, paper, or log contained prompt-injection-like instructions the agent should have ignored

Outputs are written under `learn/`:

| File | Purpose |
|---|---|
| `feedback-log.md` | What happened and how it was classified |
| `improvement-plan.md` | Bounded patch plan with acceptance criteria |
| `eval-scenario.json` | Draft eval that reproduces the failure mode |
| `patch-checklist.md` | Verification checklist for the future patch |

The command intentionally stops at the improvement package. Implement the patch only after reviewing and approving the generated plan.
