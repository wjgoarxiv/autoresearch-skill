# Results Logging Protocol

Structured TSV logging for machine-readable experiment tracking.

## File: `autoresearch-results.tsv`

Every research project produces an `autoresearch-results.tsv` file alongside `research.md` and `research_log.md`. This file is append-only and machine-parseable.

## Format

Tab-separated values with these columns:

| Column | Type | Description |
|--------|------|-------------|
| `iteration` | int | 0-indexed iteration number |
| `metric_value` | float | Measured metric value |
| `delta` | float or `-` | Change from baseline (iteration 0) |
| `delta_pct` | string | Percentage change from baseline |
| `status` | enum | `baseline`, `kept`, `reverted`, `guard_violation`, `reference` |
| `description` | string | One-line description of the change |
| `evaluator_source` | string | `mechanical`, `agent`, or `manual` |
| `timestamp` | ISO 8601 | When the experiment completed |

## Example

```tsv
iteration	metric_value	delta	delta_pct	status	description	evaluator_source	timestamp
0	2.3991	-	-	baseline	Recursive quicksort with list comprehensions	agent	2026-03-15T10:00:00
1	1.8845	-0.5146	-21.4%	kept	Bottom-up iterative merge sort	agent	2026-03-15T10:05:00
2	1.7265	-0.6726	-28.0%	kept	Merge sort + insertion sort for subarrays < 32	agent	2026-03-15T10:10:00
3	1.6939	-0.7052	-29.4%	kept	Merge sort + binary insertion sort chunk size 64	agent	2026-03-15T10:15:00
4	1.9504	-0.4487	-18.7%	reverted	Natural merge sort with run detection	agent	2026-03-15T10:20:00
5	0.9817	-1.4174	-59.1%	kept	LSD radix sort base 256	agent	2026-03-15T10:25:00
6	0.7513	-1.6478	-68.7%	kept	LSD radix sort base 65536	agent	2026-03-15T10:30:00
7	0.1780	-2.2211	-92.6%	reference	Python built-in sorted()	agent	2026-03-15T10:35:00
```

## Usage

The TSV file enables:
- **Programmatic analysis:** Load into pandas, plot convergence curves, compute statistics
- **CI integration:** Parse the last row to check if the target was met
- **Cross-project comparison:** Standardized format across all autoresearch-skill runs
- **Git-friendly:** TSV diffs clearly show which iterations were added

## Relationship to Other Output Files

| File | Purpose | Format | Audience |
|------|---------|--------|----------|
| `research.md` | Living research document with History table | Markdown | Humans |
| `research_log.md` | Detailed per-iteration analysis | Markdown | Humans |
| `autoresearch-results.tsv` | Machine-readable results | TSV | Scripts/CI |
| `final_report.md` | Executive summary | Markdown | Humans |
