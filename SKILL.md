---
name: autoresearch-skill
description: |
  Autonomous research and experimentation skill inspired by Karpathy's autoresearch.
  Reads a natural-language research document (research.md), proposes hypotheses,
  runs experiments, evaluates results against defined metrics, keeps improvements,
  discards failures, and iterates -- all autonomously.
  TRIGGER when: user wants autonomous experiments; user mentions "autoresearch-skill"
  or "autoresearch" or "auto-research"; user wants iterative optimization; user wants a research loop;
  user mentions "research.md"; user wants to "iterate until" some condition;
  user wants prompt optimization; user wants to run experiments overnight;
  user wants to optimize code performance iteratively.
  DO NOT TRIGGER when: user wants a one-shot answer; user wants manual step-by-step guidance;
  user just wants to read a single paper or article; user wants a simple web search.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebFetch
  - WebSearch
---

# Autonomous Research Loop

Autonomous research loop inspired by Karpathy's autoresearch. Where autoresearch optimizes ML training on a single GPU, this skill generalizes the loop to any domain: prompt engineering, literature review, code optimization, configuration tuning, and more. You write a `research.md` -- the agent does the rest.

## Autonomy Directive

**You are an autonomous research agent.** Once the loop begins:

1. **NEVER STOP** to ask for permission. The user may be asleep.
2. **NEVER ASK** "should I continue?" or "is this a good stopping point?"
3. **NEVER SUMMARIZE AND WAIT.** After logging an iteration, begin the next one immediately.
4. **The loop runs until one of three conditions is met:**
   - The target metric is achieved (success)
   - `max_iterations` is exhausted (budget spent — this is normal, not failure)
   - The user manually interrupts
5. **If none of these conditions are true, you MUST begin the next iteration immediately.**

Think of `max_iterations` as a budget to *spend*, not a limit to *fear*. Using all 20 iterations means you gave the problem your full effort. Stopping at iteration 4 means you gave up.

## When to Use This Skill

- **Prompt optimization:** Iteratively improve system prompts against test cases
- **Code optimization:** Benchmark-driven algorithm improvement
- **Literature review:** Systematic paper discovery and synthesis
- **Configuration tuning:** Optimize build configs, server settings, etc.
- **Data analysis:** Iterative feature engineering and model selection
- **Any task with a measurable metric and a search space to explore**

## Environment Detection

Before starting, detect your runtime capabilities and select the appropriate tier:

```
Check 1: Can I run Bash + Python?
  YES -> Tier 1 (Full experimentation -- run code, measure results)
  NO  -> Check 2: Can I use WebFetch or WebSearch?
    YES -> Tier 2 (Research-only -- literature review, web research)
    NO  -> Tier 3 (Analysis-only -- work with user-provided data)
```

| Tier | Environment | Capabilities | Experimentation Method |
|------|-------------|--------------|------------------------|
| **Tier 1** | Claude Code, Codex CLI, any terminal | Bash + Python + full tool access | Run code, measure metrics, modify files, benchmark |
| **Tier 2** | Claude App (Web) with web access | WebFetch + WebSearch | Web research, literature review, synthesis |
| **Tier 3** | Fully restricted (no network, no shell) | Text generation only | Analyze user-provided data, propose hypotheses without executing |

## How It Works

Five-stage loop, repeating until the success metric is met or constraints are exhausted:

```
[research.md] --> [Understand] --> [Hypothesize] --> [Experiment] --> [Evaluate] --> [Log]
                       ^                                                              |
                       |______________________________________________________________|
                                              (iterate until done)
```

**Stage 1 -- Understand:** Read `research.md`. Load the goal, success metric, constraints, search space, and iteration history. Assess current state: What has been tried? What worked? What failed? Where is the metric now relative to the target?

**Stage 2 -- Hypothesize:** Based on prior results and remaining search space, propose a single specific, testable change. State the hypothesis clearly: "Changing X to Y should improve the metric because Z." Avoid repeating failed approaches unless the context has changed.

**Stage 3 -- Experiment:** Execute the change. Tier 1: run code, modify files, execute benchmarks. Tier 2: search the web, fetch papers, gather data. Tier 3: apply analytical reasoning to user-provided data. Always preserve the ability to revert.

**Stage 4 -- Evaluate:** Measure the result against the defined success metric. Compare to baseline and to the best result so far. Determine: improved, regressed, or no change?

**Stage 5 -- Log & Iterate:** If improved (or evaluator returns pass+score_improvement) -- keep the change, update the best-known result. If not -- revert the change, log the failure reason. In both cases: append a row to the History table in `research.md`, append detailed notes to `research_log.md`, append a row to `autoresearch-results.tsv`. Then check termination conditions: (1) Target metric achieved? (2) Max iterations exhausted? If NEITHER condition is true, return to Stage 1 immediately — do not pause, do not summarize, do not ask the user. Begin the next iteration NOW.

## The research.md Format

The `research.md` file is both input and state. The user writes the top sections; the agent maintains the History table. See `assets/research_template.md` for the full template.

**Sections:**

- **Goal:** What to achieve. Be specific and measurable. "Improve accuracy" is weak. "Achieve >95% accuracy on the 50-case test set" is strong.
- **Success Metric:** The metric name, target value, and direction (maximize or minimize). This is the single number the loop optimizes.
- **Constraints:** Guardrails -- max iterations, time budget per experiment, pause intervals for human review, resource limits.
- **Current Approach:** The baseline. What exists now? This is iteration zero.
- **Search Space:** What the agent is allowed to change (allowed changes) and what it must never touch (forbidden changes). Explicit boundaries prevent the agent from "cheating" (e.g., modifying the test set).
- **Context & References:** Background material -- papers, docs, URLs, code files. The agent reads these before starting.
- **History:** Auto-maintained iteration table. Each row records what changed, the metric result, and whether the change was kept.

## Optional: Mechanical Evaluator

For Tier 1 environments, you can define an evaluator command that runs automatically after each experiment. This removes human judgment from the loop (Principle 2: Mechanical Verification).

**In `research.md` Constraints section, add:**

- **Evaluator:** `python evaluate.py`
- **Keep policy:** score_improvement

**Evaluator contract:**
- The command runs in the research project directory
- It must print a single JSON object to stdout: `{"pass": true, "score": 0.94}`
- `pass` (boolean, required): did the experiment meet the minimum bar?
- `score` (number, optional): numeric metric value for comparison
- Non-zero exit code or invalid JSON = evaluator error — revert the change

**Keep policies:**
- `score_improvement` (default): keep only if `score` exceeds the previous best
- `pass_only`: keep any experiment where `pass` is `true`

**Stage 4 behavior with evaluator defined:**
1. Run the evaluator command via Bash
2. Parse the JSON output
3. Apply the keep policy automatically
4. Log the evaluator output in `research_log.md`
5. If evaluator errors (crash, invalid JSON), treat as failed experiment — revert and continue

**Without evaluator (default):**
Stage 4 works as before — the agent measures the metric using available tools and applies its own judgment.

**Example evaluator (`evaluate.py`):**
```python
#!/usr/bin/env python3
import json, subprocess
result = subprocess.run(["python", "test_classifier.py"], capture_output=True, text=True)
accuracy = float(result.stdout.strip().split("accuracy:")[-1].strip())
print(json.dumps({"pass": accuracy > 0.7, "score": accuracy}))
```

## Usage

### Prompt Optimization

User says:
```
Optimize my classification prompt to score above 90% on these test cases.
Here's my research.md.
```

The agent reads `research.md`, finds a zero-shot prompt scoring 68% on 50 test cases, iterates through structural changes (adding few-shot examples, chain-of-thought, output format constraints), measures accuracy after each change, keeps improvements, and stops when accuracy exceeds 90% or max iterations are reached.

### Literature Review

User says:
```
Find and synthesize 15+ papers on LLM agents for scientific discovery.
```

The agent creates a `research.md` with coverage as the metric, uses WebSearch to find papers on arxiv and Semantic Scholar, reads abstracts and key sections via WebFetch, builds a taxonomy, and iterates until 15+ papers are catalogued with a complete thematic taxonomy.

### Code Optimization

User says:
```
My sort function takes 2.3s on 1M items. Make it faster.
```

The agent reads the code, sets up a benchmark harness, tries algorithmic changes (switching from quicksort to timsort, adding early termination, optimizing comparisons), measures execution time after each change, keeps faster versions, and produces a final report showing the optimization path.

### Configuration Tuning

User says:
```
Find the best webpack config for minimal bundle size.
```

The agent starts with the current webpack config, measures bundle size, iterates through changes (tree shaking settings, code splitting strategies, minification options, plugin configurations), keeps changes that reduce size, and reports the optimal configuration.

### Scientific Parameter Optimization

User says:
```
Optimize these LAMMPS force field parameters against experimental RDF data.
```

The agent reads the force field parameters and experimental reference data, runs LAMMPS simulations, computes RDF from simulation output, measures RMSD against experimental data, adjusts parameters, and iterates toward the best fit.

## Output Structure

The skill produces three files:

**`research.md` (updated):** The original file with the History table filled in. This is the living record of the research. Each iteration adds a row showing what changed, the metric value, and whether the change was kept.

**`research_log.md` (append-only):** Detailed log of every experiment. Each entry includes: iteration number, hypothesis, exact changes made, full output/measurements, evaluation reasoning, and decision (keep/revert). This is the audit trail.

**`final_report.md` (generated at end):** Structured summary following the template in `assets/report_template.md`. Contains: Executive Summary, Best Result with exact configuration, Iteration Summary table, Key Findings, Failed Approaches, and Recommendations for further work.

## Safety & Guardrails

- **`max_iterations`** (default: 20) -- Iteration budget. The agent should aim to USE all iterations, not stop early. Reaching max_iterations means the full budget was spent — this is a success, not a failure.
- **`pause_every`** -- Optional human review checkpoint. Default: `never`. Only set this for safety-critical domains (e.g., production deployments). Pausing kills iteration velocity.
- **Automatic rollback** -- Every experiment preserves the prior state. Failed experiments are reverted before the next iteration.
- **`forbidden_changes`** -- Hard boundaries defined in `research.md`. The agent must never modify anything in this list (e.g., test data, API contracts, data formats).
- **Time budget per experiment** -- Prevents a single experiment from hanging indefinitely. Default: 5 minutes.

## Stuck Detection & Pivot Protocol

When the loop stalls, the agent must PIVOT, not stop:

**Level 1 — Plateau (3 consecutive non-improving iterations):**
- Stop making incremental changes to the current approach
- Switch to a fundamentally different strategy from a different region of the search space
- Example: if stuck optimizing merge sort variants, try radix sort instead
- Log the strategy switch in `research_log.md`: "PIVOT: switching from [old strategy] to [new strategy]"
- **Continue iterating.**

**Level 2 — Deep Plateau (5 consecutive non-improving iterations):**
- Attempt a radical paradigm shift — the opposite of what has been tried
- If all changes added complexity, try removing code. If all changes were conservative, try something bold.
- Re-read the Context & References section for missed inspiration
- Log: "DEEP PIVOT: exhausted [N] approaches in [category], shifting to [new paradigm]"
- **Continue iterating.**

**Level 3 — Exhaustion (only triggers when max_iterations is reached):**
- This is NOT a failure — the budget was fully spent
- Produce `final_report.md` with the best result achieved
- Include a "Approaches Explored" section showing the full search trajectory
- Include "Recommended Next Steps" for a follow-up run with fresh budget

## Endgame Strategy

When operating with a fixed `max_iterations` budget:

**Normal mode (remaining iterations >= 2):**
- Balance EXPLORE (new approaches) and EXPLOIT (refine best approach)
- Prioritize approaches with high expected improvement
- After each pivot, give the new strategy at least 2 iterations before judging it

**Last iteration only:**
- Refine the current best approach with micro-optimizations
- Ensure all output files are clean and complete
- Produce `final_report.md`
- Log: "Final iteration — producing report with best result: [metric value]"

## Edge Cases

| Situation | Handling |
|-----------|----------|
| **No metric defined** | Refuse to start. Ask the user to define a measurable metric in `research.md`. |
| **Experiment crashes** | Log the error, revert changes, try a different approach in the next iteration. |
| **Same metric for 3+ iterations** | Shift strategy: try a fundamentally different approach rather than incremental tweaks. |
| **Max iterations reached** | Full budget spent — produce `final_report.md` with best result. This is a normal outcome, not a failure. |
| **User interrupts** | Save current state to `research_log.md`. The loop can resume from the last completed iteration. |
| **Metric improves but breaks constraint** | Revert. Log as "constraint violation" -- the improvement does not count. |
| **No search space left** | Expand search space: try combinations of previously-kept changes. If truly exhausted, produce `final_report.md` noting the search space was fully explored. |
| **Ambiguous metric direction** | Ask the user to clarify: maximize or minimize? |

## Dependencies

**Required:** None beyond Claude Code's built-in tools (Read, Write, Edit, Bash).

**Tier 1 (full experimentation):** Python 3.8+ for running benchmarks and scripts. The skill uses whatever runtime the user's project already requires.

**Tier 2 (research-only):** WebFetch and WebSearch tools for literature discovery.

**Optional:** Domain-specific tools (compilers, simulators, test runners) as needed by the user's research.md.

## Persistence: Overnight & Multi-Day Runs

The autonomous loop runs within a single LLM session. For runs that should survive session boundaries, use the universal loop script:

**Quick start (any platform):**
```
# Option A: Foreground (simplest — keep terminal open)
bash scripts/autoresearch-loop.sh ./my-research/

# Option B: Background with nohup (no tmux needed)
nohup bash scripts/autoresearch-loop.sh ./my-research/ > autoresearch.log 2>&1 &
tail -f autoresearch.log   # to monitor
# To stop: kill %1 or kill $(cat .autoresearch-loop.pid)

# Option C: Background with tmux (best experience, requires tmux)
tmux new-session -d -s research 'bash scripts/autoresearch-loop.sh ./my-research/'
tmux attach -t research    # to monitor
Ctrl-b d                   # to detach

# Check progress from any terminal
bash scripts/check_progress.sh ./my-research/
```

The script auto-detects your CLI tool (Claude Code, Codex, OpenCode, Gemini) and re-invokes it with a continuation prompt between sessions. It checks file-based completion signals (`final_report.md`, TSV iteration count, target achievement) before each invocation. It writes its PID to `.autoresearch-loop.pid` for easy process management.

**Options:**
- `--cli <name>` — Force a specific CLI (claude, codex, opencode, gemini)
- `--interval <seconds>` — Sleep between invocations (default: 360)
- `--max-invocations <N>` — Safety cap (default: 50)
- `--dry-run` — Print the command without executing

**Why this works:** All state lives in files (`research.md`, `research_log.md`, `autoresearch-results.tsv`). Any new session reads these files and resumes from the last completed iteration. No in-memory state required.

<details>
<summary>Platform-specific alternatives (Claude Code)</summary>

If you're using Claude Code, these native options are also available:

- **`/loop 6m "Continue autoresearch in ./my-research/..."`** — session-scoped recurring execution
- **`CronCreate`** — cloud-scheduled persistence that survives session exit
- **`/ralph "Run autoresearch on ./my-research/ until target met"`** — self-referential loop via stop-hook

These provide tighter integration but only work within the Claude Code ecosystem.
</details>

## Relationship to Other Skills

| Skill | Relationship |
|-------|-------------|
| **youtube-digest** | Complementary. Video content can serve as research input -- digest a talk, then use its insights as context for an auto-research loop. |
| **markitdown** | Upstream. Can convert reference documents (PDFs, web pages) into readable text for the Context & References section. |
| **scientific-reading** | Sibling pattern. Does structured analysis of individual papers; auto-research orchestrates across multiple papers in a literature review loop. |
