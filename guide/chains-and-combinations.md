# Chains and Combinations

## What Chaining Means

Chaining is running multiple autoresearch commands in sequence, where each command reads the files the previous one wrote. There is no in-memory state shared between commands — every command reads from disk and writes to disk.

This means chains work across sessions, terminal restarts, and machines. If a run crashes mid-chain, you resume from the last written file. Nothing is lost.

**The file-passing contract:**

| Command | Reads | Writes |
|---|---|---|
| `/autoresearch:plan` | _(wizard prompts user)_ | `research.md`, `evaluate.py` |
| `/autoresearch` | `research.md` | `research.md` (History), `research_log.md`, `autoresearch-results.tsv`, `progress.png`, `final_report.md` |
| `/autoresearch:debug` | _(symptom description)_ | `debug/findings.md`, `debug/hypotheses.md`, `debug/eliminated.md` |
| `/autoresearch:fix` | `debug/findings.md` or direct error input | `fix-results.tsv` |
| `/autoresearch:ship` | Any artifact in the working directory | `ship-log.md` |
| `/autoresearch:security` | Source files, configs | `security-report.md` |
| `/autoresearch:reason` | _(argument or question)_ | `reason-report.md` |
| `/autoresearch:predict` | _(question or document)_ | `predict-report.md` |
| `/autoresearch:scenario` | _(domain or system description)_ | `scenario-report.md` |

The simplest rule: put all files in one working directory. Each command reads what it needs and writes its output there.

---

## 8 Concrete Chain Patterns

### 1. plan → autoresearch

**Purpose:** Standard starting point — set up a research project, then run the optimization loop.

**Files flowing between commands:** plan writes `research.md` and `evaluate.py`; autoresearch reads both.

```bash
/autoresearch:plan
# Wizard produces research.md + evaluate.py with baseline score recorded

/autoresearch
# Loop reads research.md, runs experiments until target met or budget spent
```

---

### 2. autoresearch → ship

**Purpose:** Go from a completed optimization loop directly to publishing the result.

**Files flowing between commands:** autoresearch writes `final_report.md` and the optimized artifact; ship reads both.

```bash
/autoresearch
# Loop completes, writes final_report.md + best implementation

/autoresearch:ship
# 8-phase pipeline: tests, security scan, docs check, confirmation gate, publish
```

---

### 3. debug → fix → ship

**Purpose:** Go from a mysterious failure all the way to a deployed fix.

**Files flowing between commands:** debug writes `debug/findings.md`; fix reads it to implement the proposed fix; ship reads the fixed codebase.

```bash
/autoresearch:debug
# Produces debug/findings.md: confirmed root cause + minimal reproduction + proposed fix

/autoresearch:fix
# Reads debug/findings.md, implements fix iteratively, stops at 0 errors

/autoresearch:ship
# Runs full shipping pipeline on the now-fixed codebase
```

---

### 4. security → fix → security re-audit

**Purpose:** Find vulnerabilities, fix them, then confirm they are actually gone. The re-audit catches fixes that solve the symptom without solving the root cause, or introduce new vulnerabilities.

**Files flowing between commands:** security writes `security-report.md`; fix reads the HIGH-severity findings as its error list; second security pass re-reads the codebase directly.

```bash
/autoresearch:security
# STRIDE + OWASP audit → security-report.md with findings by severity

/autoresearch:fix
# Reads HIGH-severity findings from security-report.md, fixes each iteratively

/autoresearch:security
# Re-run the audit to verify fixes are effective and no regressions introduced
```

---

### 5. reason → plan → autoresearch

**Purpose:** For high-stakes optimizations where choosing the wrong approach is expensive — deliberate carefully before committing iteration budget to the loop.

**Files flowing between commands:** reason writes `reason-report.md`; the plan wizard reads it to populate search space and constraints; autoresearch runs with a well-reasoned, focused search space.

```bash
/autoresearch:reason
# Adversarial deliberation on the best approach
# Writes reason-report.md: strongest argument + weaknesses identified + counterarguments defeated

/autoresearch:plan
# Reference reason-report.md when the wizard asks about search space and constraints
# Produces research.md with a focused, prioritized search space

/autoresearch
# Loop with a well-reasoned search space — fewer wasted iterations
```

---

### 6. predict → autoresearch

**Purpose:** Form predictions about which approaches will work before committing to the loop. Use the ranked predictions to front-load the search space with highest-confidence hypotheses.

**Files flowing between commands:** predict writes `predict-report.md`; copy the top-ranked predictions into the Search Space section of `research.md` before running the loop.

```bash
/autoresearch:predict
# Multi-persona deliberation → predict-report.md with ranked hypotheses + confidence scores

# Manually copy top predictions into research.md Search Space section

/autoresearch
# Loop tries highest-confidence approaches first, spends budget more efficiently
```

---

### 7. scenario → debug

**Purpose:** Explore edge cases systematically to surface bugs before users encounter them.

**Files flowing between commands:** scenario writes `scenario-report.md` with failing scenarios across 12 dimensions; debug takes a failing scenario as its bug symptom input.

```bash
/autoresearch:scenario
# 12-dimension exploration (empty inputs, concurrency, large inputs, adversarial data...)
# Writes scenario-report.md with observed failures noted

/autoresearch:debug
# Take a failing scenario from scenario-report.md as the bug symptom
# Runs scientific root-cause analysis with falsifiable hypotheses
```

---

### 8. plan → autoresearch → ship

**Purpose:** End-to-end from nothing to published. The most common production workflow.

**Files flowing between commands:** plan writes `research.md` + `evaluate.py`; autoresearch writes `final_report.md` + best implementation; ship reads both.

```bash
/autoresearch:plan
# Wizard → research.md + evaluate.py + baseline score

/autoresearch
# Loop → final_report.md + best implementation

/autoresearch:ship
# Pipeline → published artifact
```

This is the three-command workflow from the 60-second quickstart. Each command hands off to the next via files in the working directory.

---

## Working Directory Layout

```
my-project/
  research.md               <- written by plan, read by autoresearch
  evaluate.py               <- written by plan, run by autoresearch
  research_log.md           <- written by autoresearch (append-only)
  autoresearch-results.tsv  <- written by autoresearch (append-only)
  progress.png              <- overwritten by autoresearch each iteration
  final_report.md           <- written by autoresearch at end, read by ship
  ship-log.md               <- written by ship
  predict-report.md         <- written by predict
  reason-report.md          <- written by reason
  security-report.md        <- written by security
  scenario-report.md        <- written by scenario
  debug/
    findings.md             <- written by debug, read by fix
    hypotheses.md           <- written by debug
    eliminated.md           <- written by debug
  fix-results.tsv           <- written by fix
```

If a command needs output from a previous command in a different directory, pass the path explicitly:

```bash
/autoresearch:fix ./debug/findings.md
/autoresearch:ship ./my-package/
```
