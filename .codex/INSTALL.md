# autoresearch-skill — Codex CLI Install Guide

## Quick Install

```bash
# Clone the repo
git clone https://github.com/wjgoarxiv/autoresearch-skill.git /tmp/autoresearch-skill

# Link into Codex skills directory
mkdir -p ~/.codex/skills
ln -s /tmp/autoresearch-skill ~/.codex/skills/autoresearch-skill
```

## Verify Install

```bash
python ~/.codex/skills/autoresearch-skill/scripts/init_research.py \
  --goal "test install" --metric "score" --direction maximize \
  --output /tmp/test-research && echo "OK: autoresearch-skill installed"
```

## Usage with Codex CLI

Paste the skill content directly into your Codex session, or use the `AGENTS.md` approach:

```bash
# Add to your project's AGENTS.md
cat ~/.codex/skills/autoresearch-skill/SKILL.md >> AGENTS.md
```

Then in your Codex session:
```
Use autoresearch to optimize my sort function. Target: median < 0.5s on 1M integers.
```

## Subcommands

| Command | Purpose |
|---------|---------|
| `autoresearch` | Core 5-stage research loop |
| `autoresearch:plan` | 7-step setup wizard → produces research.md |
| `autoresearch:debug` | Scientific bug hunting with falsifiable hypotheses |
| `autoresearch:fix` | Iterative error crusher, auto-stops at 0 errors |
| `autoresearch:predict` | Multi-persona deliberation with anti-herd detection |
| `autoresearch:security` | STRIDE+OWASP iterative audit |
| `autoresearch:scenario` | 12-dimension scenario exploration |
| `autoresearch:reason` | Adversarial refinement with blind-judge panel |
| `autoresearch:ship` | Universal shipping workflow (9 ship types) |

## Overnight Runs (Codex)

```bash
# Background with nohup
nohup bash scripts/autoresearch-loop.sh ./my-research/ > autoresearch.log 2>&1 &
# Monitor
bash scripts/check_progress.sh ./my-research/
```

The loop script auto-detects `codex` in PATH and uses it for invocations.

## Requirements

- Python 3.8+ (standard library only — no pip installs needed)
- Codex CLI installed and authenticated
