# autoresearch:ship — Universal Shipping Pipeline

## Purpose

`ship` is an 8-phase linear pipeline that takes any artifact from "ready to ship" to "deployed" with exactly one human gate: the irreversible publish/deploy step. Phases 1–6 run fully automatically — they verify completeness, run tests, scan for security issues, check documentation, confirm version consistency, and build the artifact. Phase 7 pauses for explicit user approval before any irreversible action. Phase 8 executes the deploy. Every checklist item is logged to `ship-log.md`, giving you an audit trail of what was verified and when. The checklist adapts to the artifact type you specify (library, CLI, API, web app, ML model, skill, docs site, infrastructure, or research paper).

## When to Use

- You want to ship a versioned artifact and need a systematic pre-release checklist run automatically.
- You want to confirm tests pass, security is clean, and docs are current before any deploy command is run.
- You want a single human approval gate (not ten separate manual checks) before publish.
- You are shipping to PyPI, npm, GitHub Releases, Vercel, AWS, HuggingFace, arXiv, or any similar target.
- You want a logged record of what was verified at ship time.

## When NOT to Use

- You are in active development and want iterative experimentation — use the main autoresearch loop.
- You have errors to fix before shipping — use `fix` first, then come back to `ship`.
- You just want a code review without executing a deploy.

## Usage

```
/autoresearch:ship
```

You will be asked:
1. What are you shipping? (library/package, CLI, REST API, web app, ML model, skill/prompt, docs site, infrastructure, or research paper)
2. Where does this deploy? (PyPI, npm, GitHub Releases, Vercel, AWS, HuggingFace, arXiv, etc.)

Then phases 1–6 run automatically. At Phase 7 you will see a pre-deploy summary and must type **"SHIP IT"** to proceed. "ok", "sure", or "yes" are not accepted — only the explicit phrase.

## Output

| File | Content |
|------|---------|
| `ship-log.md` | Phase-by-phase log: each checklist item as PASS/FAIL, test counts, security findings, version confirmation, build output, user approval timestamp, deploy command and exit code |

## Example

**Domain:** Publishing a Python CLI tool to PyPI.

```
Phase 1 — Verify: all source files present, no TODO in production paths — PASS
Phase 2 — Tests: 142 passed, 0 failed (14.3s) — PASS
Phase 3 — Security: pip audit: 0 HIGH, 0 CRITICAL — PASS
Phase 4 — Docs: README with install + quickstart present, CHANGELOG updated for v1.2.0 — PASS
Phase 5 — Version: 1.2.0 consistent across pyproject.toml, __init__.py, CHANGELOG — PASS

== READY TO SHIP ==
Artifact: CLI tool — mypackage
Version:  1.2.0
Deploy to: PyPI
Tests:    142 passed
Security: 0 blockers
Build:    dist/ 1.1MB

Type "SHIP IT" to proceed.
```

User types: `SHIP IT`

```
Phase 8: twine upload dist/* → exit 0
Published: https://pypi.org/project/mypackage/1.2.0/
```

## Tips

- Phase 6 version bump is a confirmation step, not an auto-bump. The agent will ask "The current version is X. Is this correct?" before proceeding — do not assume it will increment the version for you.
- If Phase 2 fails, the pipeline stops. Use `/autoresearch:fix` to resolve the errors, then re-run `/autoresearch:ship` from the start — it will re-verify cleanly.
- The only valid response at Phase 7 is "SHIP IT" (case-insensitive). This is intentional friction. If you find yourself typing it without confidence, treat that hesitation as a signal to address the concern before proceeding.
