# autoresearch-skill vs uditgoenka/autoresearch

## Why We Built This

[Karpathy's autoresearch](https://github.com/karpathy/autoresearch) sparked the idea: what if an AI agent could run ML experiments overnight, fully autonomously, without human checkpoints? That 630-line framework crystallized a loop — hypothesize, experiment, evaluate, keep or revert — that applies far beyond ML training.

[uditgoenka/autoresearch](https://github.com/uditgoenka/autoresearch) (3,183 stars) took that idea and built a polished implementation with strong community adoption and GitHub Actions integration. It is an excellent tool for its target use case.

This skill was built to answer a different question: **what does that loop look like when you need it to work on any LLM CLI platform, across any domain, with a mechanical evaluator and zero dependencies?** The result is less a fork and more a parallel design with different tradeoffs.

---

## Side-by-Side Comparison

| Capability | uditgoenka/autoresearch | autoresearch-skill (this repo) |
|:-----------|:------------------------|:-------------------------------|
| **Multi-platform support** | Primarily Claude Code | Claude Code + Codex CLI + OpenCode + Gemini CLI |
| **Mechanical evaluator** | LLM self-reports results | Strict `{"pass": bool, "score": number}` contract — no LLM judgment in keep/revert |
| **Zero dependencies** | Requires specific npm/pip setup | Python 3.8+ stdlib only — no pip installs |
| **Non-English documentation** | English only | Korean README (`README-Ko-KR.md`) included |
| **Command count** | Single main command | 9 active subcommands + 1 planned (`/autoresearch:learn`) |
| **Overnight scripts** | Platform-specific | Cross-platform bash (`autoresearch-loop.sh` + `check_progress.sh`) |
| **Plugin marketplace** | Not supported | `.claude-plugin/plugin.json` + `skills/` directory |
| **Subcommand architecture** | Monolithic | Modular skill files per subcommand (`skills/debug/`, `skills/fix/`, etc.) |
| **GitHub Actions integration** | Yes — first-class | Not built-in (TSV output enables custom CI integration) |
| **Community / stars** | ~3,183 stars, active community | Early-stage, growing |
| **Worked examples with real data** | Template-based | 4 examples with measured before/after results and charts |
| **Stuck / plateau detection** | Basic retry | 3-level pivot: strategy shift → paradigm shift → finalize |
| **Scaffolding tool** | Manual setup | `init_research.py` generates ready-to-run project in seconds |
| **Machine-readable audit trail** | Log files | Append-only `autoresearch-results.tsv` + `research_log.md` |

---

## When to Choose uditgoenka/autoresearch

- Your team is already on Claude Code and wants a battle-tested, community-supported tool
- You need GitHub Actions integration out of the box
- You prefer a larger community with more examples and issue history
- Star count and ecosystem maturity matter for your project's credibility

## When to Choose autoresearch-skill

- You work across multiple LLM CLI platforms (Codex, OpenCode, Gemini CLI) and need one skill that works everywhere
- You want the mechanical evaluator contract (`{"pass": bool, "score": number}`) to remove LLM judgment from keep/revert decisions — critical for reproducibility
- Your research domain is not a code project: simulation sweeps, literature gaps, prompt tuning, function fitting
- You need overnight runs that survive session restarts across platforms via the bash loop script
- Zero pip dependencies is a hard requirement (air-gapped environments, corporate policy)
- You want modular subcommands — `debug`, `fix`, `predict`, `security`, `scenario`, `reason`, `ship` — as separate skills you can invoke independently
- Korean documentation is useful for your team

---

## Honest Acknowledgments

uditgoenka/autoresearch has ~3,183 stars for good reasons. It has broader community adoption, more real-world validation, and GitHub Actions support that this skill does not provide. If your workflow is Claude Code + GitHub Actions and you want the most-used implementation, that repo is a reasonable default.

This skill makes different bets: platform portability, strict mechanical evaluation, and a subcommand architecture that lets each research mode be a standalone skill. Those bets are worth it for specific use cases and may not matter for yours.

---

## Evaluator Contract Detail

The core differentiator is the evaluator output format. autoresearch-skill enforces:

```json
{"pass": true, "score": 0.94}
```

- `pass` (bool) — determines keep vs. revert. No ambiguity.
- `score` (number) — logged to TSV, used for plateau detection and progress plots.

Any evaluator that outputs this JSON works: Python scripts, shell one-liners, or compiled binaries. The skill never asks the LLM "was this better?" — the evaluator decides.

---

## Repository Structure (autoresearch-skill)

```
autoresearch-skill/
├── SKILL.md                  # Root skill with command routing
├── skills/
│   ├── autoresearch/         # Core 5-stage loop
│   ├── plan/                 # Setup wizard
│   ├── debug/                # Bug hunting
│   ├── fix/                  # Error crusher
│   ├── predict/              # Forecasting
│   ├── security/             # STRIDE + OWASP audit
│   ├── scenario/             # Scenario exploration
│   ├── reason/               # Adversarial reasoning
│   └── ship/                 # Shipping workflow
├── scripts/
│   ├── init_research.py      # Project scaffolding
│   ├── autoresearch-loop.sh  # Overnight cross-platform loop
│   └── check_progress.sh     # Progress checker
├── .claude-plugin/           # Plugin marketplace manifest
├── examples/                 # 4 worked examples with real data
└── assets/                   # Charts and visual evidence
```
