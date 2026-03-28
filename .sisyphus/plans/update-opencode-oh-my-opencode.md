# Update OpenCode and Oh My OpenCode

## TL;DR
> **Summary**: Safely update the user's current standalone OpenCode install and the active `oh-my-opencode` plugin/config stack in place, with preservation-first backups, command-based validation, and explicit rollback paths.
> **Deliverables**:
> - Verified preflight inventory and effective-config map
> - Timestamped backup set for all rollback-relevant files
> - Updated OpenCode binary with recorded before/after versions
> - Refreshed `oh-my-opencode` install that preserves current plugin entries and agent model assignments
> - Post-update smoke-test evidence and rollback matrix
> **Effort**: Short
> **Parallel**: YES - 4 waves
> **Critical Path**: 1 -> 2 -> 4 -> 5 -> 6 -> 7 -> 8

## Context
### Original Request
Help update the currently used OpenCode and `oh-my-openagent`, and set up plan(s) for the work.

### Interview Summary
- The active local target is `oh-my-opencode`, not a separately discovered `oh-my-openagent` package.
- The user chose one safe update now, not a broader maintenance SOP.
- The user chose a backup-first, in-place update strategy.
- Current environment facts:
  - `opencode --version` returns `1.3.3`.
  - The binary resolves to `/Users/woojin/.opencode/bin/opencode`.
  - `/Users/woojin/.config/opencode/opencode.json` loads `"oh-my-opencode@latest"`, `"opencode-openai-codex-auth"`, and `file:///Users/woojin/.config/opencode/plugins/codex-quota.js`.
  - `/Users/woojin/.config/opencode/oh-my-opencode.json` contains custom agent/category model mappings that must be preserved.
  - Existing `*.bak` files and `switch-config.sh` provide partial rollback support.

### Metis Review (gaps addressed)
- Do not assume update method from binary location alone; detect and record it before mutation.
- Preserve the entire plugin array and the existing `oh-my-opencode.json` model assignments; do not reconfigure providers unless validation proves a breakage.
- Treat `package.json`, `bun.lock`, mode-switch config files, and any project-level `.opencode` overrides as part of the rollback surface.
- Separate rollback into three domains: OpenCode binary rollback, plugin/config rollback, and config-mode rollback.

## Work Objectives
### Core Objective
Produce and execute a safe, backup-first in-place update runbook for the user's current OpenCode + `oh-my-opencode` environment without losing custom config, extra plugins, or recovery options.

### Deliverables
- Preflight report with effective config sources, binary path, install method, current versions, and project override status
- Timestamped backup directory containing all rollback-relevant files
- Updated OpenCode binary with before/after version evidence
- Refreshed `oh-my-opencode` installation with preserved config semantics
- Post-update verification bundle and rollback instructions tied to captured pre-update state

### Definition of Done (verifiable conditions with commands)
- `opencode --version` returns a single version string and differs from the preflight version, or matches the chosen explicit target version.
- A timestamped backup directory exists under `~/.config/opencode/backups/` and contains the required files.
- `/Users/woojin/.config/opencode/opencode.json` still contains the exact three plugin entries in the expected order.
- `/Users/woojin/.config/opencode/oh-my-opencode.json` still preserves the existing custom agent/category mapping keys.
- `bash /Users/woojin/.config/opencode/switch-config.sh status` returns a `[STATUS]` line.
- No provider re-auth flow is required unless a smoke test explicitly fails.

### Must Have
- Backup before any mutation
- Explicit install-method detection before OpenCode upgrade
- Preservation-first handling of `oh-my-opencode.json`
- Verification after each mutation step
- Rollback commands that point to actual captured backup paths and pre-update versions

### Must NOT Have (guardrails, AI slop patterns, scope boundaries)
- No migration from `oh-my-opencode` naming/config to a different product name
- No auth reconfiguration unless validation proves auth is broken
- No dropping or reordering the existing plugin array entries
- No silent overwriting of curated agent model mappings
- No declaration of success based only on command exit without config verification

## Verification Strategy
> ZERO HUMAN INTERVENTION - all verification is agent-executed.
- Test decision: none; this is an operational update runbook verified with command-based smoke checks and config assertions
- QA policy: Every task includes happy-path and failure-path agent-executed scenarios
- Evidence: `.sisyphus/evidence/task-{N}-{slug}.{ext}`

## Execution Strategy
### Parallel Execution Waves
> Shared read-only discovery is front-loaded for parallelism; mutating update steps remain gated and serial.

Wave 1: inventory current state, detect overrides, resolve update method/targets
Wave 2: create rollback snapshot and validate backup completeness
Wave 3: update OpenCode and verify runtime/config integrity
Wave 4: refresh `oh-my-opencode`, run smoke checks, and validate rollback paths

### Dependency Matrix (full, all tasks)
- 1 -> blocks 2, 3, 4
- 2 -> blocks 5, 6, 7, 8
- 3 -> blocks 4
- 4 -> blocks 5
- 5 -> blocks 6, 7, 8
- 6 -> blocks 7
- 7 -> blocks 8
- 8 -> final verification gate

### Agent Dispatch Summary (wave -> task count -> categories)
- Wave 1 -> 3 tasks -> `quick`, `unspecified-high`
- Wave 2 -> 1 task -> `quick`
- Wave 3 -> 2 tasks -> `unspecified-high`
- Wave 4 -> 2 tasks -> `unspecified-high`, `deep`

## TODOs
> Implementation + Test = ONE task. Never separate.
> EVERY task MUST have: Agent Profile + Parallelization + QA Scenarios.

- [ ] 1. Capture preflight inventory and effective config sources

  **What to do**: Record the current OpenCode version, binary path, shell path resolution, current plugin array, current `oh-my-opencode` config keys, existing backup files, and whether any project-level `.opencode` overrides exist in the target working directory. Save the report to `.sisyphus/evidence/task-1-preflight.txt`.
  **Must NOT do**: Do not mutate any config, auth, plugin, or binary during this task.

  **Recommended Agent Profile**:
  - Category: `quick` - Reason: Read-only environment inspection with deterministic commands
  - Skills: `[]` - No extra skill is needed
  - Omitted: `["git-master"]` - No git work is involved

  **Parallelization**: Can Parallel: YES | Wave 1 | Blocks: 2, 3, 4 | Blocked By: none

  **References**:
  - Pattern: `/Users/woojin/.config/opencode/opencode.json:2` - OpenCode user config schema and plugin array location
  - Pattern: `/Users/woojin/.config/opencode/opencode.json:3` - Exact plugin entries that must survive the update
  - Pattern: `/Users/woojin/.config/opencode/oh-my-opencode.json:3` - Start of curated agent mappings that must be preserved
  - Pattern: `/Users/woojin/.config/opencode/package.json:2` - Local plugin dependency state

  **Acceptance Criteria** (agent-executable only):
  - [ ] `opencode --version > .sisyphus/evidence/task-1-opencode-version.txt` exits 0
  - [ ] `python3 - <<'PY'
import json, pathlib, shutil, os
root = pathlib.Path('/Users/woojin/.config/opencode')
cfg = json.loads((root/'opencode.json').read_text())
omo = json.loads((root/'oh-my-opencode.json').read_text())
print(shutil.which('opencode'))
print(os.path.realpath(shutil.which('opencode')))
print(cfg['plugin'])
print(sorted(list(omo.get('agents', {}).keys()))[:5])
PY > .sisyphus/evidence/task-1-preflight.txt` exits 0
  - [ ] `python3 - <<'PY'
from pathlib import Path
matches = list(Path('/Users/woojin/Desktop/02_Areas/01_Codes_automation/14_autoresearch-skill').glob('**/.opencode/**'))
print(len(matches))
PY > .sisyphus/evidence/task-1-project-overrides.txt` exits 0

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Happy path preflight capture
    Tool: Bash
    Steps: Run the inventory commands above and write all outputs to the evidence files.
    Expected: All files are created and contain version/path/plugin/config-source data.
    Evidence: .sisyphus/evidence/task-1-preflight.txt

  Scenario: Missing config file detection
    Tool: Bash
    Steps: Run `test -f /Users/woojin/.config/opencode/opencode.json && test -f /Users/woojin/.config/opencode/oh-my-opencode.json`.
    Expected: Exit code 0; otherwise stop the plan before any update.
    Evidence: .sisyphus/evidence/task-1-preflight-error.txt
  ```

  **Commit**: NO | Message: `n/a` | Files: none

- [ ] 2. Create timestamped rollback snapshot

  **What to do**: Create `BACKUP_DIR="$HOME/.config/opencode/backups/pre-update-$(date +%Y%m%d-%H%M%S)"` and copy every rollback-relevant file into it: `opencode.json`, `oh-my-opencode.json`, `package.json`, `bun.lock` if present, all `oh-my-opencode.*.json` mode files, `switch-config.sh`, and any `*.bak` files already in `~/.config/opencode/`.
  **Must NOT do**: Do not start any update command before backup completeness is validated.

  **Recommended Agent Profile**:
  - Category: `quick` - Reason: Deterministic file snapshot work
  - Skills: `[]` - No extra skill is needed
  - Omitted: `["playwright"]` - No browser work is involved

  **Parallelization**: Can Parallel: NO | Wave 2 | Blocks: 5, 6, 7, 8 | Blocked By: 1

  **References**:
  - Pattern: `/Users/woojin/.config/opencode/switch-config.sh:10` - Config directory and target file naming
  - Pattern: `/Users/woojin/.config/opencode/switch-config.sh:13` - Existing mode-switch rollback posture
  - Pattern: `/Users/woojin/.config/opencode/oh-my-opencode.normal.json:1` - Alternate mode configs must be included
  - Pattern: `/Users/woojin/.config/opencode/oh-my-opencode.spark-exhausted.json:1` - Alternate mode configs must be included

  **Acceptance Criteria** (agent-executable only):
  - [ ] `python3 - <<'PY'
from pathlib import Path
root = Path('/Users/woojin/.config/opencode')
required = ['opencode.json', 'oh-my-opencode.json', 'package.json', 'switch-config.sh']
print(all((root/f).exists() for f in required))
PY` prints `True`
  - [ ] Backup command exits 0 and writes the chosen backup path to `.sisyphus/evidence/task-2-backup-dir.txt`
  - [ ] `python3 - <<'PY'
from pathlib import Path
backup_dir = Path(open('.sisyphus/evidence/task-2-backup-dir.txt').read().strip())
expected = {'opencode.json','oh-my-opencode.json','package.json','switch-config.sh'}
present = {p.name for p in backup_dir.iterdir()}
print(expected.issubset(present))
PY > .sisyphus/evidence/task-2-backup-check.txt` prints `True`

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Happy path backup snapshot
    Tool: Bash
    Steps: Create BACKUP_DIR, copy the required files, and record the path and directory listing.
    Expected: Backup directory exists and contains the required files before any mutation begins.
    Evidence: .sisyphus/evidence/task-2-backup-check.txt

  Scenario: Backup completeness failure
    Tool: Bash
    Steps: Run the subset-check assertion immediately after copying.
    Expected: If the result is not True, stop the plan and do not proceed to update commands.
    Evidence: .sisyphus/evidence/task-2-backup-error.txt
  ```

  **Commit**: NO | Message: `n/a` | Files: none

- [ ] 3. Resolve OpenCode update method and target version

  **What to do**: Determine the exact update method to use for this machine before changing anything. Prefer the native OpenCode self-upgrade path, but record the binary location, available fallback methods, and the chosen target version in evidence. If a specific target is not required, use the latest stable version available at execution time.
  **Must NOT do**: Do not assume Homebrew or curl-only management from path inspection alone; record the decision rationale.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: Operational decision point with external-doc grounding
  - Skills: `[]` - No extra skill is needed
  - Omitted: `["doctor"]` - Diagnosis is not the main purpose here

  **Parallelization**: Can Parallel: YES | Wave 1 | Blocks: 4 | Blocked By: 1

  **References**:
  - Pattern: `/Users/woojin/.config/opencode/temp_search_repo/docs/guide/installation.md:68` - OpenCode presence check pattern
  - External: `https://opencode.ai/docs/cli/` - Official `opencode upgrade` command surface
  - External: `https://opencode.ai/install` - Official installer script and versioned install options
  - External: `https://github.com/anomalyco/opencode/releases/latest` - Latest stable release target

  **Acceptance Criteria** (agent-executable only):
  - [ ] Chosen update method and target version are written to `.sisyphus/evidence/task-3-update-method.txt`
  - [ ] `.sisyphus/evidence/task-3-update-method.txt` includes all of: current version, binary path, chosen command, rollback command source
  - [ ] The chosen command is one of: `opencode upgrade`, `opencode upgrade --method ...`, or a version-pinned equivalent documented by OpenCode

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Happy path method selection
    Tool: Bash
    Steps: Record `opencode --version`, binary path, and the exact upgrade command that will be used.
    Expected: Evidence file contains a single explicit command with rationale and rollback note.
    Evidence: .sisyphus/evidence/task-3-update-method.txt

  Scenario: Unsupported method ambiguity
    Tool: Bash
    Steps: If no supported official method can be selected confidently, stop before mutation and record the blocker.
    Expected: No update command runs until one official method is chosen.
    Evidence: .sisyphus/evidence/task-3-update-method-error.txt
  ```

  **Commit**: NO | Message: `n/a` | Files: none

- [ ] 4. Upgrade OpenCode and capture before-after version evidence

  **What to do**: Execute the chosen OpenCode upgrade command from Task 3, then capture the post-upgrade version, binary path, and any installer output needed for rollback traceability.
  **Must NOT do**: Do not continue if the version command fails after upgrade or if the binary path changes unexpectedly without explanation.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: Mutating toolchain update with immediate verification needs
  - Skills: `[]` - No extra skill is needed
  - Omitted: `["playwright"]` - No UI automation is needed

  **Parallelization**: Can Parallel: NO | Wave 3 | Blocks: 5 | Blocked By: 1, 3

  **References**:
  - External: `https://opencode.ai/docs/cli/` - Official `opencode upgrade` semantics
  - External: `https://github.com/anomalyco/opencode/releases/latest` - Stable target check
  - Pattern: `/Users/woojin/.config/opencode/temp_search_repo/README.md:385` - Local warning that older OpenCode versions can break config; verify the result is newer than the bad range

  **Acceptance Criteria** (agent-executable only):
  - [ ] The chosen upgrade command exits 0 and logs output to `.sisyphus/evidence/task-4-opencode-upgrade.txt`
  - [ ] `opencode --version > .sisyphus/evidence/task-4-opencode-version-after.txt` exits 0
  - [ ] `python3 - <<'PY'
from pathlib import Path
before = Path('.sisyphus/evidence/task-1-opencode-version.txt').read_text().strip()
after = Path('.sisyphus/evidence/task-4-opencode-version-after.txt').read_text().strip()
print(before != after or after)
PY > .sisyphus/evidence/task-4-opencode-version-compare.txt` produces a non-empty value

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Happy path OpenCode upgrade
    Tool: Bash
    Steps: Run the selected official upgrade command, then run `opencode --version` and capture output.
    Expected: Upgrade command exits 0 and version output is available immediately afterward.
    Evidence: .sisyphus/evidence/task-4-opencode-upgrade.txt

  Scenario: Broken binary after upgrade
    Tool: Bash
    Steps: Run `opencode --version` immediately after upgrade.
    Expected: If it fails, stop the plan and restore using the binary rollback path recorded in Task 3.
    Evidence: .sisyphus/evidence/task-4-opencode-upgrade-error.txt
  ```

  **Commit**: NO | Message: `n/a` | Files: none

- [ ] 5. Verify OpenCode still loads the expected user config and plugin array

  **What to do**: After the OpenCode upgrade, verify that the active user-scoped config still exists, the plugin array still contains the exact three entries in the same order, and the mode switcher still reports a valid status.
  **Must NOT do**: Do not start the `oh-my-opencode` refresh until these assertions pass.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: Post-upgrade integrity gate before secondary mutation
  - Skills: `[]` - No extra skill is needed
  - Omitted: `["git-master"]` - No repository work is involved

  **Parallelization**: Can Parallel: NO | Wave 3 | Blocks: 6, 7, 8 | Blocked By: 2, 4

  **References**:
  - Pattern: `/Users/woojin/.config/opencode/opencode.json:3` - Exact expected plugin array
  - Pattern: `/Users/woojin/.config/opencode/switch-config.sh:26` - Status command behavior and expected `[STATUS]` output
  - Pattern: `/Users/woojin/.config/opencode/oh-my-opencode.json:106` - Existing `google_auth` and agent config should remain present after OpenCode update

  **Acceptance Criteria** (agent-executable only):
  - [ ] `python3 - <<'PY'
import json
with open('/Users/woojin/.config/opencode/opencode.json') as f:
    data = json.load(f)
expected = [
  'oh-my-opencode@latest',
  'opencode-openai-codex-auth',
  'file:///Users/woojin/.config/opencode/plugins/codex-quota.js',
]
print(data.get('plugin') == expected)
PY > .sisyphus/evidence/task-5-plugin-array-check.txt` prints `True`
  - [ ] `bash /Users/woojin/.config/opencode/switch-config.sh status > .sisyphus/evidence/task-5-switch-status.txt` exits 0
  - [ ] `python3 - <<'PY'
from pathlib import Path
print(Path('/Users/woojin/.config/opencode/opencode.json').exists() and Path('/Users/woojin/.config/opencode/oh-my-opencode.json').exists())
PY > .sisyphus/evidence/task-5-config-exists.txt` prints `True`

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Happy path config integrity gate
    Tool: Bash
    Steps: Run the plugin-array assertion, file existence assertion, and switch-config status command.
    Expected: Plugin array check is True, both config files exist, and switch-config output starts with `[STATUS]`.
    Evidence: .sisyphus/evidence/task-5-plugin-array-check.txt

  Scenario: Plugin drift after OpenCode update
    Tool: Bash
    Steps: Compare the live `plugin` array to the expected array.
    Expected: If the result is not True, stop and restore `opencode.json` from the backup before any plugin refresh.
    Evidence: .sisyphus/evidence/task-5-plugin-array-error.txt
  ```

  **Commit**: NO | Message: `n/a` | Files: none

- [ ] 6. Prepare a preservation-first oh-my-opencode refresh command

  **What to do**: Build the exact installer command that will refresh `oh-my-opencode` without redefining the current environment. Preserve the existing `oh-my-opencode.json` as authoritative, preserve the current plugin array, and avoid auth steps unless they become necessary after smoke checks. Use `bunx oh-my-opencode install` by default, with `npx` only if Bun is unavailable.
  **Must NOT do**: Do not let the installer redefine current model/provider choices from scratch.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: Non-trivial config-preservation planning around an installer workflow
  - Skills: `[]` - No extra skill is needed
  - Omitted: `["doctor"]` - This task is preparation, not diagnosis

  **Parallelization**: Can Parallel: NO | Wave 4 | Blocks: 7 | Blocked By: 2, 5

  **References**:
  - Pattern: `/Users/woojin/.config/opencode/temp_search_repo/docs/guide/installation.md:16` - Recommended installer entrypoint is `bunx oh-my-opencode install`
  - Pattern: `/Users/woojin/.config/opencode/temp_search_repo/docs/guide/installation.md:87` - Non-interactive installer pattern with provider flags
  - Pattern: `/Users/woojin/.config/opencode/temp_search_repo/docs/guide/installation.md:251` - Do not change model settings or disable features unless explicitly requested
  - Pattern: `/Users/woojin/.config/opencode/oh-my-opencode.json:3` - Current config is curated and must remain the source of truth

  **Acceptance Criteria** (agent-executable only):
  - [ ] A single explicit refresh command is written to `.sisyphus/evidence/task-6-omo-refresh-command.txt`
  - [ ] `.sisyphus/evidence/task-6-omo-refresh-command.txt` names the runtime (`bunx` or `npx`), includes `install`, and explains why no auth change is planned
  - [ ] The task records a config-preservation rule set in `.sisyphus/evidence/task-6-omo-preservation-rules.txt`

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Happy path refresh command preparation
    Tool: Bash
    Steps: Detect whether `bunx` exists; if yes, choose `bunx oh-my-opencode install`, else `npx oh-my-opencode install`. Record the chosen command and preservation rules.
    Expected: A single command and rule set are written before execution begins.
    Evidence: .sisyphus/evidence/task-6-omo-refresh-command.txt

  Scenario: Missing runtime for installer
    Tool: Bash
    Steps: Check `command -v bunx || command -v npx`.
    Expected: If neither exists, stop and record the blocker before attempting a refresh.
    Evidence: .sisyphus/evidence/task-6-omo-refresh-error.txt
  ```

  **Commit**: NO | Message: `n/a` | Files: none

- [ ] 7. Refresh oh-my-opencode and diff against the preserved baseline

  **What to do**: Run the chosen installer command from Task 6, then compare the resulting `opencode.json` and `oh-my-opencode.json` against the backup copies. Allow only expected changes related to version refresh; stop and restore from backup if plugin array entries, agent mapping keys, or local plugin references drift.
  **Must NOT do**: Do not accept installer-generated config churn that changes provider/model decisions without an explicit need.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: Mutating plugin refresh with strict config-diff gating
  - Skills: `[]` - No extra skill is needed
  - Omitted: `["playwright"]` - No browser automation should occur unless auth is proven broken

  **Parallelization**: Can Parallel: NO | Wave 4 | Blocks: 8 | Blocked By: 2, 5, 6

  **References**:
  - Pattern: `/Users/woojin/.config/opencode/opencode.json:3` - Plugin array that must not drift
  - Pattern: `/Users/woojin/.config/opencode/oh-my-opencode.json:3` - Curated agent mappings that must remain present
  - Pattern: `/Users/woojin/.config/opencode/temp_search_repo/package.json:3` - Local mirrored package version reference (`3.2.2`) for sanity checks
  - Pattern: `/Users/woojin/.config/opencode/temp_search_repo/docs/guide/installation.md:99` - Installer responsibilities and config registration behavior

  **Acceptance Criteria** (agent-executable only):
  - [ ] The installer command exits 0 and writes output to `.sisyphus/evidence/task-7-omo-refresh.txt`
  - [ ] `python3 - <<'PY'
import json
backup_dir = open('.sisyphus/evidence/task-2-backup-dir.txt').read().strip()
with open('/Users/woojin/.config/opencode/opencode.json') as f: live = json.load(f)
with open(f'{backup_dir}/opencode.json') as f: old = json.load(f)
expected = old['plugin']
print(live.get('plugin') == expected)
PY > .sisyphus/evidence/task-7-plugin-preservation.txt` prints `True`
  - [ ] `python3 - <<'PY'
import json
backup_dir = open('.sisyphus/evidence/task-2-backup-dir.txt').read().strip()
with open('/Users/woojin/.config/opencode/oh-my-opencode.json') as f: live = json.load(f)
with open(f'{backup_dir}/oh-my-opencode.json') as f: old = json.load(f)
print(set(old.get('agents', {}).keys()).issubset(set(live.get('agents', {}).keys())))
print(set(old.get('categories', {}).keys()).issubset(set(live.get('categories', {}).keys())))
PY > .sisyphus/evidence/task-7-omo-key-preservation.txt` prints two `True` lines

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Happy path oh-my-opencode refresh
    Tool: Bash
    Steps: Run the prepared installer command, then run the plugin-preservation and key-preservation assertions.
    Expected: Installer exits 0, plugin preservation is True, and both key-preservation checks are True.
    Evidence: .sisyphus/evidence/task-7-omo-refresh.txt

  Scenario: Installer overwrites curated config
    Tool: Bash
    Steps: Run the preservation assertions immediately after install.
    Expected: If any assertion fails, restore `opencode.json` and `oh-my-opencode.json` from BACKUP_DIR before continuing.
    Evidence: .sisyphus/evidence/task-7-omo-refresh-error.txt
  ```

  **Commit**: NO | Message: `n/a` | Files: none

- [ ] 8. Run final smoke checks and validate rollback commands

  **What to do**: Perform the final post-update verification bundle: version check, plugin-array assertion, agent/category key-preservation assertion, `switch-config.sh status`, and a recorded rollback matrix containing the exact restore commands for configs and the exact prior OpenCode version noted in preflight.
  **Must NOT do**: Do not rely on subjective “looks fine” checks or user confirmation.

  **Recommended Agent Profile**:
  - Category: `deep` - Reason: Final correctness gate across multiple rollback domains
  - Skills: `[]` - No extra skill is needed
  - Omitted: `["requesting-code-review"]` - This is an operational runbook check, not a source-code review

  **Parallelization**: Can Parallel: NO | Wave 4 | Blocks: Final Verification Wave | Blocked By: 2, 5, 7

  **References**:
  - Pattern: `/Users/woojin/.config/opencode/switch-config.sh:26` - Status output contract for config-mode rollback verification
  - Pattern: `/Users/woojin/.config/opencode/opencode.json:3` - Final plugin array contract
  - External: `https://opencode.ai/docs/cli/` - Version verification command surface
  - External: `https://github.com/anomalyco/opencode/releases/latest` - Latest stable comparison target

  **Acceptance Criteria** (agent-executable only):
  - [ ] `opencode --version > .sisyphus/evidence/task-8-final-version.txt` exits 0
  - [ ] The plugin-array assertion from Task 5 still prints `True` after the plugin refresh
  - [ ] The key-preservation assertion from Task 7 still prints only `True` lines
  - [ ] `bash /Users/woojin/.config/opencode/switch-config.sh status > .sisyphus/evidence/task-8-switch-status.txt` exits 0
  - [ ] A rollback matrix is written to `.sisyphus/evidence/task-8-rollback-matrix.md` with exact backup paths and restore commands

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Happy path final smoke test
    Tool: Bash
    Steps: Re-run the final version check, plugin-array assertion, key-preservation assertion, and switch-config status command.
    Expected: All commands succeed and all assertions remain true after the full update flow.
    Evidence: .sisyphus/evidence/task-8-final-version.txt

  Scenario: Rollback readiness check
    Tool: Bash
    Steps: Verify that the rollback matrix file exists and references the recorded BACKUP_DIR and pre-update OpenCode version.
    Expected: The rollback file is complete enough to execute without new discovery.
    Evidence: .sisyphus/evidence/task-8-rollback-matrix.md
  ```

  **Commit**: NO | Message: `n/a` | Files: none

## Final Verification Wave (4 parallel agents, ALL must APPROVE)
- [ ] F1. Plan Compliance Audit - oracle
- [ ] F2. Code Quality Review - unspecified-high
- [ ] F3. Real Manual QA - unspecified-high
- [ ] F4. Scope Fidelity Check - deep

## Commit Strategy
- Commit: NO
- Reason: This plan updates user-scoped tooling/config outside the current repo; no git commit should be made unless the user later asks to version the runbook changes.

## Success Criteria
- The user can update OpenCode and `oh-my-opencode` in place without losing custom config or extra plugins.
- The runbook captures before/after state, backup paths, and deterministic rollback commands.
- The update result is validated with command-based checks, not subjective inspection.
