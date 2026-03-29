<p align="center"><img src="./cover.png" width="100%" /></p>

<h1 align="center">autoresearch-skill</h1>
<p align="center">
  <em>Define a goal. Let the agent research, experiment, and iterate -- autonomously.</em>
</p>
<p align="center">
  <a href="#quick-start">Quick Start</a> · <a href="#features">Features</a> · <a href="#usage">Usage</a> · <a href="./README-Ko-KR.md">한국어</a>
</p>
<p align="center">
  <img src="https://img.shields.io/github/stars/wjgoarxiv/autoresearch-skill?style=social" />
  <img src="https://img.shields.io/badge/license-MIT-blue" />
  <img src="https://img.shields.io/badge/python-3.8+-green" />
  <img src="https://img.shields.io/badge/skill-Claude%20Code-blueviolet" />
</p>

---

### autoresearch-skill in Action

| | Without autoresearch-skill | With autoresearch-skill |
|:---:|:---:|:---:|
| **Code Optimization** | ![](./examples/comparison_figures/code_without.png) | ![](./examples/comparison_figures/code_with.png) |
| **Literature Review** | ![](./examples/comparison_figures/lit_without.png) | ![](./examples/comparison_figures/lit_with.png) |
| **Prompt Optimization** | ![](./examples/comparison_figures/prompt_without.png) | ![](./examples/comparison_figures/prompt_with.png) |
| **Skill Elaboration** | ![](./examples/comparison_figures/skill_without.png) | ![](./examples/comparison_figures/skill_with.png) |
| **Function Fitting** | Baseline: `y = x` (RMSE 2.11) | 4-freq Fourier model (RMSE 0.034), 18 iterations with mechanical evaluator |

> [!NOTE]
> An LLM skill that turns natural-language research goals into autonomous experiment-evaluate-iterate loops -- inspired by [Karpathy's autoresearch](https://github.com/karpathy/autoresearch). Write a `research.md`, and the agent handles hypothesis generation, experimentation, evaluation, and iteration. Works with Claude Code, Codex CLI, and Gemini CLI.

## Features

- **Karpathy-Inspired Loop** -- Autonomous experiment -> evaluate -> keep/revert cycle, generalized beyond ML training
- **Natural Language Programming** -- `research.md` is your program: define goals, metrics, and constraints in plain English
- **Zero Dependencies** -- Python stdlib only. No pip packages required for core functionality
- **Multi-Agent Compatible** -- Works with Claude Code, Codex CLI, and Gemini CLI out of the box
- **Automatic Rollback** -- Failed experiments are reverted automatically; only improvements are kept
- **Full Audit Trail** -- Every iteration logged to `research_log.md` with timestamps, changes, and results
- **3 Tier Environment Detection** -- Adapts to your runtime: full experimentation (Tier 1), research-only (Tier 2), or analysis-only (Tier 3)
- **Safety Built In** -- Max iterations, pause-for-review intervals, forbidden-change boundaries, and time budgets

## Why This Skill?

Other autoresearch implementations provide the loop concept. This repo provides the **complete toolkit**:

- **5 worked examples** with real measured data -- not templates, not placeholders
- **Visual evidence** -- before/after charts, optimization trajectories, error heatmaps
- **Multi-agent compatible** -- works with Claude Code, Codex CLI, and Gemini CLI
- **Copy-paste install** -- one block, paste into your LLM chat, done
- **Scaffolding tool** -- `init_research.py` creates a ready-to-run research project in seconds
- **Core principles** -- 8 formalized Karpathy principles with practical mapping to `research.md`
- **Stuck detection** -- automatic strategy shifts when the loop plateaus
- **Endgame strategy** -- switches from explore to exploit when iterations are running out
- **TSV logging** -- machine-readable `autoresearch-results.tsv` for CI integration and analysis

## Quick Start

### Copy-Paste Install

> [!TIP]
> Works with any LLM CLI that supports skills (Claude Code, Codex, Gemini CLI). Just paste the block below into your chat.

```
I want to install the autoresearch-skill. Do these steps:
1. git clone https://github.com/wjgoarxiv/autoresearch-skill.git /tmp/autoresearch-skill
2. mkdir -p ~/.claude/skills/autoresearch-skill && cp -r /tmp/autoresearch-skill/SKILL.md /tmp/autoresearch-skill/scripts /tmp/autoresearch-skill/assets ~/.claude/skills/autoresearch-skill/
3. Test: python ~/.claude/skills/autoresearch-skill/scripts/init_research.py --goal "test" --metric "score" --direction maximize --output /tmp/test-research && echo "OK: autoresearch-skill installed"
4. Say "autoresearch-skill installed successfully"
```

### Manual Install

```bash
# Clone the repo
git clone https://github.com/wjgoarxiv/autoresearch-skill.git
cd autoresearch-skill

# Symlink into your skills directory
mkdir -p ~/.claude/skills
ln -s "$(pwd)" ~/.claude/skills/autoresearch-skill

# No pip dependencies needed!
```

### Other Tools

| Tool | Skills Path | Install Command |
|------|-------------|-----------------|
| **Claude Code** | `~/.claude/skills/autoresearch-skill/` | See above |
| **Codex CLI** | `~/.codex/skills/autoresearch-skill/` | `mkdir -p ~/.codex/skills && ln -s "$(pwd)" ~/.codex/skills/autoresearch-skill` |
| **Gemini CLI** | `~/.gemini/skills/autoresearch-skill/` | `mkdir -p ~/.gemini/skills && ln -s "$(pwd)" ~/.gemini/skills/autoresearch-skill` |

## Installation

Copy this skill into your CLI tool's skills directory:

| Platform | Command |
|----------|---------|
| **Claude Code** | `cp -r autoresearch-skill/ ~/.claude/skills/autoresearch-skill/` |
| **Codex CLI** | `cp -r autoresearch-skill/ ~/.codex/skills/autoresearch-skill/` |
| **OpenCode** | `cp -r autoresearch-skill/ ~/.config/opencode/skills/autoresearch-skill/` |
| **Gemini CLI** | `cp -r autoresearch-skill/ ~/.gemini/skills/autoresearch-skill/` |

Or clone directly:
```bash
git clone https://github.com/wjgoarxiv/autoresearch-skill.git
cp -r autoresearch-skill/ ~/.claude/skills/   # adjust path for your platform
```

The skill is automatically discovered when you mention "autoresearch" or "research.md" in your prompt.

## Usage

### 1. Prompt Optimization

```
My customer support classifier prompt scores 68% accuracy.
Use auto-research to optimize it above 90% on these 50 test cases.
```

### 2. Literature Review

```
Research the latest advances in "LLM agents for scientific discovery".
Find and synthesize at least 15 papers from 2024-2026.
```

### 3. Code Optimization

```
My sort function takes 2.3s on 1M items. Use auto-research to make it faster.
Target: under 0.5 seconds. Pure Python only, no C extensions.
```

### 4. Configuration Tuning

```
Find the optimal webpack config for my project.
Metric: minimize gzipped bundle size. Constraint: all e2e tests must pass.
```

### 5. Scaffold a New Research Project

```bash
python scripts/init_research.py \
  --goal "Optimize database query performance" \
  --metric "query_time_ms" \
  --direction minimize \
  --target "< 50" \
  --output ./db-research/
```

## Overnight Runs

To run autoresearch overnight (or for days), use the universal loop script:

```bash
# 1. Set up your research project
python scripts/init_research.py --goal "..." --metric "..." --direction maximize --output ./my-research/

# 2. Start the overnight loop (pick one)

# Option A: Keep terminal open (simplest)
bash scripts/autoresearch-loop.sh ./my-research/

# Option B: Background without tmux
nohup bash scripts/autoresearch-loop.sh ./my-research/ > autoresearch.log 2>&1 &

# Option C: Background with tmux (best experience)
tmux new-session -d -s research 'bash scripts/autoresearch-loop.sh ./my-research/'

# 3. Check progress anytime
bash scripts/check_progress.sh ./my-research/
```

The script auto-detects your CLI tool and handles session restarts, completion detection, and safety limits. Works with Claude Code, Codex CLI, OpenCode, and Gemini CLI. No dependencies beyond bash.

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                     research.md                             │
│  (Goal, Metric, Constraints, Search Space, History)         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      v
            ┌─────────────────┐
            │  1. UNDERSTAND   │  Read research.md + history
            └────────┬────────┘
                     v
            ┌─────────────────┐
            │  2. HYPOTHESIZE  │  Propose a testable change
            └────────┬────────┘
                     v
            ┌─────────────────┐
            │  3. EXPERIMENT   │  Execute: run code / search / analyze
            └────────┬────────┘
                     v
            ┌─────────────────┐
         ┌──│  4. EVALUATE     │──┐
         │  └─────────────────┘  │
     improved?                not improved?
         │                       │
    ┌────v────┐            ┌─────v─────┐
    │  KEEP   │            │  REVERT   │
    └────┬────┘            └─────┬─────┘
         │                       │
         └──────────┬────────────┘
                    v
            ┌─────────────────┐
            │ 5. LOG & ITERATE │──→ Back to step 1
            └─────────────────┘    (or STOP if done)
```

## Output Format

The skill produces three files:

| File | Purpose | Grows? |
|------|---------|--------|
| `research.md` | Living research document with iteration history | Updated each iteration |
| `research_log.md` | Detailed append-only experiment log | Append only |
| `final_report.md` | Structured summary with best result and insights | Generated at end |

## Environment Tiers

The skill automatically detects your runtime capabilities:

| Tier | Environment | Capabilities | Use Case |
|------|-------------|--------------|----------|
| **Tier 1** | Claude Code, Codex CLI, terminal | Bash + Python + full tools | Run experiments, benchmark, modify files |
| **Tier 2** | Claude App with web access | WebFetch + WebSearch | Literature review, web research |
| **Tier 3** | Restricted (no shell, no network) | Text generation | Analyze user data, propose hypotheses |

## Requirements

| Requirement | Details |
|-------------|---------|
| **Python** | 3.8+ (stdlib only) |
| **LLM CLI** | Claude Code, Codex CLI, or Gemini CLI |
| **Domain tools** | Varies by use case (e.g., Python for code optimization, web access for lit review) |

## Inspired By

[Karpathy's autoresearch](https://github.com/karpathy/autoresearch) -- a 630-line framework where an AI agent autonomously runs ML experiments overnight. This skill generalizes that loop to any domain where you have a measurable goal and a search space to explore.

## Contributing

Contributions welcome! Ideas for new example `research.md` templates are especially appreciated.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-example`)
3. Commit your changes (`git commit -m 'Add amazing example'`)
4. Push to the branch (`git push origin feature/amazing-example`)
5. Open a Pull Request

## License

MIT -- see [LICENSE](./LICENSE) for details.
