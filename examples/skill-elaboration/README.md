# Example: Skill Elaboration

Goal: improve a PDF/P&ID analysis skill by adding concrete domain-specific instructions and measurable structure.

| Field | Value |
|---|---|
| Metric | Structural skill quality score (`quality_score`, maximize) |
| Evaluator | `python evaluate.py` |
| Baseline | 0.2750 |
| Best result | 0.9767 |
| Iterations logged | 2 |
| Visual result | [`results.png`](./results.png) |

## Expected Output

- [`research.md`](./research.md): improvement goal and allowed skill-edit scope
- [`research_log.md`](./research_log.md): rationale for each skill edit
- [`autoresearch-results.tsv`](./autoresearch-results.tsv): score trace
- [`original_skill/SKILL.md`](./original_skill/SKILL.md): baseline skill
- [`improved_skill/SKILL.md`](./improved_skill/SKILL.md): improved output
- [`final_report.md`](./final_report.md): summary of structural improvements

This example is useful when evaluating whether autoresearch can improve prompts, skills, rubrics, or other structured natural-language artifacts.
