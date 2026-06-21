# Research Report: {Title}

**Generated:** {date}
**Total Iterations:** {n}
**Final Metric:** {best value} ({direction}: {metric name})
**Status:** {completed | max_iterations_reached | user_stopped}

---

## Executive Summary
{2-3 sentence summary of what was researched, the best result achieved, and key insight.}

## Best Result
- **Iteration:** #{n}
- **Change:** {what was different from baseline}
- **Metric Value:** {value} (baseline: {baseline}, improvement: {delta})
- **Configuration/Code:** {the winning setup}

## Iteration Summary
| # | Change | Metric | vs Baseline | Kept? |
|---|--------|--------|-------------|-------|
{rows}

## Key Findings
1. {Pattern or insight discovered during experimentation}
2. {What worked consistently}
3. {Surprising result}

## Failed Approaches
1. {What was tried and why it didn't work}
2. {Dead ends worth documenting}

## Pivot History
- {When the loop detected a plateau, what strategy changed?}

## Reproducibility Commands
```bash
{commands to reproduce the best metric and guard checks}
```

## Artifact Checklist
- [ ] `research.md` includes the final history row
- [ ] `research_log.md` records the evaluator output for each iteration
- [ ] `autoresearch-results.tsv` has the standard 8-column header
- [ ] `progress.png` or final visualization is present when plotting is available
- [ ] Best result can be reproduced with the commands above

## Recommendations
- {Next steps if the user wants to continue}
- {Related areas to explore}
