# Draft: Update OpenCode and oh-my-openagent

## Requirements (confirmed)
- [request]: Help update the currently used `OpenCode` and `oh-my-openagent`.
- [request]: Help set up plan(s) for the update work.

## Technical Decisions
- [approach]: Explore actual local installation/update paths before proposing any update procedure.
- [scope assumption]: Treat `oh-my-openagent` as `oh-my-opencode` unless the user confirms a different tool name.

## Research Findings
- [workspace]: No existing `.sisyphus/` directory was present in this repo at planning start.
- [repo]: Current workspace is `autoresearch-skill`, so update steps may depend on external/global installs rather than this repo.
- [local opencode]: User has a real OpenCode config tree at `/Users/woojin/.config/opencode/`.
- [plugin config]: `/Users/woojin/.config/opencode/opencode.json` loads `"oh-my-opencode@latest"` plus local plugins.
- [omo config]: `/Users/woojin/.config/opencode/oh-my-opencode.json` is active and backed by multiple `*.bak` files plus alternate mode configs.
- [switcher]: `/Users/woojin/.config/opencode/switch-config.sh` already supports normal / spark-exhausted / emergency config switching.
- [plugin pkg]: `/Users/woojin/.config/opencode/package.json` pins `@opencode-ai/plugin` at `1.2.21`.
- [local docs]: `/Users/woojin/.config/opencode/temp_search_repo/README.md` states Oh My OpenCode 3.0 is stable and recommends `oh-my-opencode@latest` installation.
- [local docs]: `/Users/woojin/.config/opencode/temp_search_repo/docs/guide/installation.md` exists and should be used as the authoritative install/update reference.
- [rollback posture]: Existing local evidence supports backup/rollback planning through config backups and documented keep/revert patterns, but no complete target-specific update SOP is already written.

## Open Questions
- [goal]: Is the target only updating the tools, or also establishing an ongoing repeatable update/verification workflow?
- [risk tolerance]: Should the plan prefer in-place update, side-by-side reinstall, or backup-first replacement?

## Scope Boundaries
- INCLUDE: Discover current install method, define update sequence, define verification and rollback.
- EXCLUDE: Executing the update during planning.
