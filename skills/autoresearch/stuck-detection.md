# Stuck Detection & Pivot Protocol

When the loop stalls, the agent must PIVOT, not stop.

## Level Definitions

### Level 1 — Plateau (3 consecutive non-improving iterations)

**Trigger:** 3 iterations in a row where the metric does not improve (kept or reverted, no progress).

**Action:**
1. Stop making incremental changes to the current approach
2. Switch to a fundamentally different strategy from a different region of the search space
3. Example: if stuck optimizing merge sort variants, try radix sort instead
4. Log in `research_log.md`: `"PIVOT: switching from [old strategy] to [new strategy]"`
5. **Continue iterating.** Do not stop. Do not summarize. Do not ask the user.

**Pivot strategies (try in order if still stuck):**
- Change the algorithm family entirely (e.g., sort: comparison → counting)
- Reduce scope (do less but more efficiently)
- Change representation (e.g., data structure)
- Try the opposite approach (if adding was failing, try removing)

### Level 2 — Deep Plateau (5 consecutive non-improving iterations)

**Trigger:** 5 iterations in a row with no improvement.

**Action:**
1. Attempt a radical paradigm shift — the opposite of what has been tried
2. If all changes added complexity → try removing code
3. If all changes were conservative → try something bold
4. Re-read the Context & References section of `research.md` for missed inspiration
5. Try combining near-misses: if two approaches each got 50% of the way, combine them
6. Log: `"DEEP PIVOT: exhausted [N] approaches in [category], shifting to [new paradigm]"`
7. **Continue iterating.** The budget is not yet exhausted.

**Additional Level 2 strategies:**
- Revisit the baseline — is the problem statement itself wrong?
- Try a completely different evaluation approach (if manual, try scripted; if scripted, recheck the script)
- Apply the inverse: optimize in the direction you haven't tried
- "Combine near-misses": find iterations where metric was close — try merging their changes

### Level 3 — Exhaustion (max_iterations reached)

**Trigger:** `max_iterations` is reached.

**This is NOT a failure.** The budget was fully spent.

**Action:**
1. Produce `final_report.md` with the best result achieved
2. Include "Approaches Explored" section: full search trajectory
3. Include "Recommended Next Steps" for a follow-up run with fresh budget
4. Mark the loop as complete

## Counting Rules

- **Non-improving** means: metric did not improve vs. the current best (whether kept or reverted)
- **Reset the counter** whenever an improvement is found (counter back to 0)
- **Do not reset** when a new strategy is tried but doesn't improve (the plateau continues)
- **Count across strategy switches** at Level 2: even after a Level 1 pivot, the Level 2 counter keeps counting

## Log Format

Every pivot must be logged in `research_log.md` with this format:

```
## PIVOT (Level 1) — Iteration N
- Previous strategy: [description]
- Reason: [N] consecutive non-improving iterations
- New strategy: [description]
- Expected direction: [why this might work]
```

```
## DEEP PIVOT (Level 2) — Iteration N
- Exhausted approaches: [list]
- New paradigm: [description]
- Inspiration source: [where this idea came from]
```

## Example Pivot Sequences

**Code optimization (sort algorithm):**
```
Iterations 1-3: Quicksort variants → PLATEAU
PIVOT (Level 1): Switch to merge sort family
Iterations 4-6: Merge sort variants → PLATEAU
PIVOT (Level 1): Switch to radix sort
Iterations 7-9: Radix sort (base 256, 65536) → IMPROVING → reset counter
...
```

**Prompt optimization:**
```
Iterations 1-3: Adding examples to prompt → PLATEAU
PIVOT (Level 1): Try chain-of-thought structure
Iterations 4-8: CoT variants → PLATEAU
DEEP PIVOT (Level 2): Try removing all instructions, minimal prompt
Iteration 9: Minimal prompt → IMPROVING → reset counter
```
