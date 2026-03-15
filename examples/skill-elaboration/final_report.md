# Final Report: P&ID Skill Elaboration

## Executive Summary

The autoresearch-skill system improved the `/pdf` skill's P&ID diagram analysis capability from **20.8% to 93.8%** composite score across **9 iterations** (v0 through v8), a **+73.0 percentage point** improvement. The target of 85% was met at iteration v6 and exceeded in subsequent endgame iterations. One iteration (v3) was reverted after regression, triggering the stuck detection system which successfully guided a strategy shift.

## Best Result

- **Version:** v8 (final polish)
- **Composite Score:** 93.8%
- **Streams Found:** 14/15
- **Streams Numbered:** 13/14
- **Equipment Found:** 8/8

## Iteration Summary

| Iter | Score | Delta | Streams | Numbered | Equipment | Status | Key Change |
|------|-------|-------|---------|----------|-----------|--------|------------|
| v0 | 20.8% | -- | 4/15 | 0/4 | 3/8 | baseline | Original /pdf skill |
| v1 | 33.3% | +12.5pp | 7/15 | 0/7 | 4/8 | kept | Visual element recognition |
| v2 | 55.0% | +21.7pp | 10/15 | 4/10 | 6/8 | kept | P&ID symbol definitions |
| v3 | 43.3% | -11.7pp | 8/15 | 2/8 | 5/8 | REVERTED | Step-by-step algorithm (Stuck Detection L1) |
| v4 | 65.0% | +10.0pp | 11/15 | 7/11 | 7/8 | kept | Simplified connection rules |
| v5 | 77.1% | +12.1pp | 12/15 | 10/12 | 7/8 | kept | ISA-5.1 numbering convention |
| v6 | 85.5% | +8.4pp | 13/15 | 11/13 | 8/8 | kept | Flow direction inference (TARGET MET) |
| v7 | 90.0% | +4.5pp | 14/15 | 13/14 | 8/8 | kept | Endgame: bypass detection + JSON output |
| v8 | 93.8% | +3.8pp | 14/15 | 13/14 | 8/8 | kept | Final polish: stuck detection notes + cleanup |

## Key Findings

### 1. Symbol definitions are the highest-impact single change (+21.7pp)

Iteration v2 added a table mapping visual symbols to equipment types (pump = circle with arrow, tank = cylinder, valve = bowtie). This single addition produced the largest improvement of any iteration. The LLM fundamentally cannot identify equipment it has no visual vocabulary for. Providing a lookup table transforms the task from open-ended visual interpretation to pattern matching against known definitions.

### 2. Rules outperform algorithms for LLM instructions

Iteration v3 added a detailed 12-step algorithmic procedure for stream tracing. It caused a regression of -11.7pp. The replacement (v4) used three simple declarative rules and improved by +21.7pp over the reverted version. LLMs execute declarative rules naturally but struggle with multi-step procedural logic that requires maintaining state across steps. This finding applies broadly to any LLM skill that involves visual or structural analysis.

### 3. Stuck detection successfully triggered strategy shift

When v3 regressed below v2, the stuck detection system identified this as a Level 1 (Plateau) condition and initiated a strategy shift. Instead of attempting to fix the algorithm (which would have continued down a counterproductive path), the system pivoted to a fundamentally different approach (simplified rules). This demonstrates that stuck detection is not just a safety mechanism but an active contributor to finding better solutions.

### 4. Endgame strategy preserved gains without regression risk

After v6 met the 85% target with fewer than 3 iterations remaining, the system switched from explore mode to exploit mode. Iterations v7 and v8 made no risky structural changes, instead refining edge cases and output quality. Both iterations improved the score without any regression. The endgame strategy is essential for converting a good result into a robust one.

### 5. ISA-5.1 naming convention unlocks numbering accuracy

Iteration v5 added a formal stream numbering convention based on the ISA-5.1 standard. This improved numbering from 7/11 to 10/12 (a jump from 64% to 83% numbering accuracy). The convention also had a secondary effect: the systematic process-area-based numbering forced the LLM to scan the diagram more methodically, finding 1 additional stream. Formal conventions serve as both output formatting rules and implicit verification checklists.

### 6. Structured JSON output improves systematic detection

The JSON output template introduced in v7 forced the LLM to enumerate streams in a structured format rather than producing free-text descriptions. This systematic enumeration caught 1 additional stream and improved numbering from 11/13 to 13/14. Structured output formats are not just presentation -- they change how the LLM organizes its analysis.

## Failed Approach Analysis

### v3: Step-by-Step Stream Tracing Algorithm

**What was tried:** A 12-step procedural algorithm for tracing streams from line segments to classified, numbered streams.

**Why it failed:** LLMs process instructions differently than code interpreters. The algorithm required maintaining state (current segment, visited nodes, branch stack) across multiple steps, which the LLM could not do reliably. The result was confusion: the LLM partially executed some steps, skipped others, and produced worse results than simpler declarative rules.

**Lesson:** When writing LLM instructions, prefer "what is true" (rules) over "what to do" (algorithms). The LLM should recognize patterns, not execute procedures.

## Irreducible Error

The final skill identifies 14 of 15 streams (93.3% stream detection rate). The single missed stream is a bypass line connecting the M-box/valve assembly area to a downstream mixing point. This bypass line is visually ambiguous -- it could be interpreted as an instrument connection rather than a process stream. Correctly classifying it requires knowledge of the process design intent (the bypass exists to allow flow to continue when the valve assembly is being maintained), which is not available from the diagram alone.

This represents an irreducible error for purely visual analysis. Resolving it would require either process design documentation or domain expert annotation.

## Recommendations

1. **Always include symbol definition tables** when creating LLM skills for engineering diagram analysis. This is the single highest-leverage addition.

2. **Use declarative rules, not procedural algorithms** for LLM instructions involving visual or structural analysis.

3. **Enable stuck detection** in the autoresearch-skill loop. The v3 reversion and subsequent recovery demonstrate its value.

4. **Use endgame strategy** when the target is met with remaining iteration budget. Exploit mode preserves gains safely.

5. **Include structured output templates** in skills that require systematic enumeration. JSON schemas improve both accuracy and consistency.

6. **Accept irreducible error** when it stems from information not present in the input. Attempting to eliminate it risks overfitting to a specific diagram.

## Improvement Trajectory

```
v0  [====                              ]  20.8%  baseline
v1  [=======                           ]  33.3%  +12.5pp
v2  [==============                    ]  55.0%  +21.7pp  (highest delta)
v3  [===========                       ]  43.3%  -11.7pp  REVERTED
v4  [=================                 ]  65.0%  +10.0pp
v5  [====================              ]  77.1%  +12.1pp
v6  [======================            ]  85.5%  +8.4pp   TARGET MET
v7  [========================          ]  90.0%  +4.5pp   endgame
v8  [=========================         ]  93.8%  +3.8pp   final
```

## New Feature Utilization

| Feature | Where Used | Impact |
|---------|-----------|--------|
| Stuck Detection (L1: Plateau) | v3 regression triggered strategy shift to v4 | Prevented continued investment in counterproductive algorithm approach |
| Endgame Strategy | v7-v8 switched from explore to exploit | +8.3pp total gain with zero regression risk |
| TSV Logging | `autoresearch-results.tsv` | Full audit trail of all 9 iterations with timestamps and deltas |
| Core Principles (Karpathy) | Throughout | Simplicity-first principle directly motivated v3 reversion |
