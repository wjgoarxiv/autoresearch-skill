# Contributing to autoresearch-skill

## How to Add a New Example

Each example lives in `examples/<name>/` and must include the following files:

| File | Required | Description |
|------|----------|-------------|
| `research.md` | Yes | The research document used during the run (goal, metric, constraints, history) |
| `evaluate.py` | Yes* | Evaluator script outputting `{"pass": bool, "score": number}` where `score` is higher-is-better. Use a shell alternative if Python is not appropriate. |
| `research_log.md` | Yes | Snippet of the actual log (at least 3 iterations showing keep/revert decisions) |
| `results.png` | Yes | Before/after chart or optimization trajectory plot |
| `autoresearch-results.tsv` | Yes | TSV log with columns: `iteration`, `metric_value`, `delta`, `delta_pct`, `status`, `description`, `evaluator_source`, `timestamp` |
| `README.md` | Recommended | One paragraph describing the problem, the result, and why this example is interesting |

*If the domain does not use Python, replace `evaluate.py` with the equivalent evaluator and document the format in the example's `README.md`.

### Example Checklist

Before opening a PR with a new example:

- [ ] `research.md` shows real goal, metric, and at least 5 history rows
- [ ] `evaluate.py` (or equivalent) outputs valid `{"pass": bool, "score": number}` JSON
- [ ] `research_log.md` includes at least 3 complete iteration entries
- [ ] `results.png` shows measured data (not a placeholder or mock)
- [ ] `autoresearch-results.tsv` has a header row and at least 5 data rows
- [ ] Numbers in the example are real — tested locally, not fabricated

---

## How to Write a New Subcommand Skill

New subcommands live in `skills/<name>/SKILL.md`. Follow this structure:

### Required Frontmatter

```yaml
---
name: autoresearch:<name>
description: |
  One sentence describing what this subcommand does.
  TRIGGER when: <precise trigger conditions>
  DO NOT TRIGGER when: <anti-trigger conditions>
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebFetch    # only if needed
  - WebSearch   # only if needed
---
```

### Required Sections

1. **Purpose** — one paragraph describing the problem this subcommand solves
2. **Autonomy Directive** — copy from `SKILL.md` root (never stop, never ask permission, loop until done)
3. **Loop / Procedure** — numbered stages with explicit entry and exit conditions
4. **Output Contract** — what files are created or modified, and their format
5. **Chaining** — which subcommands this one feeds into or receives from

### Naming Convention

- Directory: `skills/<name>/` — lowercase, no hyphens (e.g., `skills/debug/`, `skills/fix/`)
- Skill file: `skills/<name>/SKILL.md`
- Invocation: `/autoresearch:<name>` — matches directory name exactly
- Add the command to the routing table in the root `SKILL.md`

### Style Rules

- Write in imperative present tense: "Read the file." not "The agent should read the file."
- No filler phrases ("Note that...", "It's important to..."). State facts directly.
- Every loop must have an explicit termination condition.
- Every output file must be described with its format and whether it is append-only or overwritten.

---

## PR Checklist

Before submitting a pull request, verify all of the following:

- [ ] `python scripts/init_research.py --help` runs without error on Python 3.8
- [ ] No new pip dependencies introduced (stdlib only)
- [ ] All new Python is compatible with Python 3.8+ (no walrus operator, no `match`, no `3.9+` type hints)
- [ ] New skill files include required frontmatter with trigger and anti-trigger conditions
- [ ] New examples include all required files (see table above) with real measured data
- [ ] Existing tests pass: `python -m pytest tests/` (if tests directory exists)
- [ ] No debug output left in scripts (`print` statements used for progress are fine; `import pdb` is not)
- [ ] PR description states what problem the change solves and links to any relevant issue

---

## Code Style

**Python**
- Target Python 3.8+ compatibility throughout
- No new `pip` dependencies — stdlib only (`os`, `json`, `subprocess`, `pathlib`, `argparse`, `csv`, etc.)
- Use `pathlib.Path` over `os.path` for new code
- Keep functions under 40 lines; split if longer
- Test with `python scripts/init_research.py --help` before submitting

**Shell scripts**
- Target `bash` (not `zsh` or `fish`)
- Use `#!/usr/bin/env bash` shebang
- `set -euo pipefail` at the top of every new script
- Quote all variable expansions: `"$var"` not `$var`

**Markdown / Skill files**
- Use ATX headings (`##`) not setext (`---` underlines)
- Tables must have a header row and alignment separator row
- No trailing whitespace
- Prefer plain ASCII diagrams (using `┌`, `│`, `└`, `─`, `v`) over images for logic flows

---

## Getting Help

Open an issue with the `question` label. For new example ideas, open a discussion before writing code — the example should demonstrate a genuinely different domain or evaluation strategy than the existing four.
