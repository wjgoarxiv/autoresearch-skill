# autoresearch:plan — Research Setup Wizard

## Purpose

`plan` is a 7-step interactive wizard that produces a complete, ready-to-run `research.md` before a single experiment is executed. It walks you through goal clarification, metric definition, search space mapping, constraints, evaluator design, and baseline measurement — then writes the file. The intent is to front-load all the ambiguity resolution that would otherwise cause the research loop to stall mid-run. A well-formed `research.md` is the difference between a focused 20-iteration run and a wandering one that never converges.

## When to Use

- You have a fuzzy optimization goal ("make this faster", "improve quality") and need to sharpen it before running experiments.
- You are starting a new research project with no `research.md` yet.
- You want to define a measurable success metric and baseline before the loop runs.
- You need to set hard constraints (forbidden files, max iterations, time budget) before the agent has free rein.
- You want to design or validate an `evaluate.py` script before the loop calls it 20 times.

## When NOT to Use

- A `research.md` already exists and you want to run the loop — invoke the loop directly instead.
- You want a one-shot answer to a question, not iterative optimization.
- You want to debug a bug, not tune a metric (use `debug` for that).

## Usage

```
/autoresearch:plan
```

The wizard asks one step at a time — never batches all questions. You will be asked:

1. What are you trying to improve? What does success look like in concrete terms?
2. What is the single number that determines pass/fail? What direction (maximize/minimize)?
3. What files/parameters can the agent modify? What must never change?
4. How many iterations? Attended or unattended? Any resource limits?
5. Can the metric be measured by a script? (If yes, an `evaluate.py` will be written.)
6. Run the evaluator now to confirm a baseline (mandatory before writing `research.md`).
7. Write `research.md` with all fields populated.

## Output

| File | Content |
|------|---------|
| `research.md` | Fully populated: goal, metric, target, search space, constraints, history table with baseline (iteration 0) |
| `evaluate.py` | Automated evaluator script (only if you chose automated evaluation in step 5) |

`research.md` will have no `TBD` or `TODO` placeholders. The history table starts with iteration 0 (your confirmed baseline).

## Example

**Domain:** Prompt engineering for a customer-support LLM.

- Goal: Improve LLM-judge satisfaction score on 50-case eval set from 6.2 to 8.0+.
- Metric: `satisfaction_score`, direction: maximize, target: 8.0.
- Allowed changes: `system_prompt.txt`, `few_shot_examples/`.
- Forbidden: eval set, production inference code.
- Evaluator: `python evaluate.py` prints `{"pass": true, "score": 8.3}`.
- Baseline run: score = 6.2 confirmed.

The wizard writes `research.md` with all of the above, plus the next-step command to launch the loop.

## Tips

- If your metric is noisy (LLM judge, timing), set `noise_runs: 3` when asked — the evaluator will median across 3 runs, preventing false progress signals.
- For overnight runs, the wizard prints the `nohup` command. Copy it directly — the path is already populated.
- Chain suggestion: after the loop finishes, run `/autoresearch:ship` to publish results. The wizard reminds you of this at the end.
