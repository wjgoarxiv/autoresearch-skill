# autoresearch:fix — Iterative Error-Crusher Loop

## Purpose

`fix` is an autonomous loop that counts errors, prioritizes them by dependency order, applies the minimal fix to the highest-priority error, recounts, and repeats until the error count reaches zero. It is cascade-aware: if nine errors stem from a single broken import, it fixes the import first and lets the dependents resolve automatically. The loop enforces a strict anti-pattern blocklist — it will not suppress, hide, or work around errors. Every iteration is logged to `fix-results.tsv` so you have a complete audit trail of what changed and why.

## When to Use

- You have a codebase with multiple errors (TypeScript compiler, pytest, cargo build, pylint, etc.) and want them systematically eliminated.
- A test suite is failing and you want the production code fixed, not the tests modified.
- You want to eliminate linter errors across a large file set without manual triage.
- You have cascading errors where fixing one is likely to resolve several others.
- You want an error elimination run that you can walk away from and return to a clean state.

## When NOT to Use

- You have a single obvious bug with a known fix — just fix it directly.
- You want root-cause investigation before fixing (use `debug` first, then `fix`).
- You want a code review without actual changes being made.

## Usage

```
/autoresearch:fix
```

You will be asked one question: "What command reveals the errors?" (e.g., `pytest`, `tsc`, `cargo build`, `pylint src/`). That command becomes the loop's oracle — it runs before and after every fix.

Default budget: 20 iterations. Override by specifying a number when invoking.

## Output

| File | Content |
|------|---------|
| `fix-results.tsv` | Tab-separated log: iteration, errors_before, errors_after, fix_applied, status |

Status values: `improved`, `done`, `no_change`, `blocked`, `budget_exhausted`.

## Example

**Domain:** TypeScript monorepo with 12 compiler errors after a refactor.

```
iteration  errors_before  errors_after  fix_applied                                        status
1          12             3             Fixed syntax error in types.ts (missing brace)      improved
2          3              1             Fixed null check in userService.ts:42               improved
3          1              0             Fixed missing import in index.ts                    done
```

The agent identified that 9 of the 12 errors were "cannot find name X" because `types.ts` had a syntax error. It fixed `types.ts` first, recounted (3 remaining), then addressed those individually.

## Anti-Pattern Blocklist

The following are strictly forbidden — the agent will skip any fix that requires them:

| Forbidden pattern | Why |
|-------------------|-----|
| `except: pass` or `except Exception: pass` | Silences errors without handling them |
| Commenting out a failing assertion | Assertions exist to catch real bugs |
| Deleting a test to make it pass | Tests are the specification |
| `# type: ignore` without explanation | Masks type errors without understanding them |
| `@pytest.mark.skip` without a linked issue | Permanently hides failures |
| Changing error thresholds to match broken output | Moves the goalposts |

If a real fix is not possible in the current iteration, the error is logged as `BLOCKED` and the loop tries other errors instead.

## Tips

- If an error count increases after a fix, the agent reverts the change automatically and tries a different approach.
- Errors that persist for 3 iterations are marked `BLOCKED` and skipped — the loop does not get stuck retrying the same approach.
- `fix` pairs naturally with `debug`: use `debug` to identify the root cause, then `fix` to eliminate all resulting errors systematically.
