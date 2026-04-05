# autoresearch-skill — OpenCode Install Guide

## Quick Install

```bash
# Clone the repo
git clone https://github.com/wjgoarxiv/autoresearch-skill.git /tmp/autoresearch-skill

# Link into OpenCode skills directory
mkdir -p ~/.opencode/skills
ln -s /tmp/autoresearch-skill ~/.opencode/skills/autoresearch-skill
```

## Verify Install

```bash
python ~/.opencode/skills/autoresearch-skill/scripts/init_research.py \
  --goal "test install" --metric "score" --direction maximize \
  --output /tmp/test-research && echo "OK: autoresearch-skill installed"
```

## Usage with OpenCode

Reference the skill in your OpenCode session:

```
Load skill from ~/.opencode/skills/autoresearch-skill/SKILL.md
Then: Use autoresearch to optimize my classifier above 95% accuracy.
```

Or use `init_research.py` to scaffold a research project first:

```bash
python ~/.opencode/skills/autoresearch-skill/scripts/init_research.py \
  --goal "Optimize webpack bundle size" \
  --metric "bundle_size_kb" \
  --direction minimize \
  --target "< 200" \
  --output ./webpack-research/
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

## Overnight Runs (OpenCode)

```bash
# Background with nohup
nohup bash scripts/autoresearch-loop.sh ./my-research/ > autoresearch.log 2>&1 &
# Monitor
bash scripts/check_progress.sh ./my-research/
```

The loop script auto-detects `opencode` in PATH and uses it for invocations.

## Requirements

- Python 3.8+ (standard library only — no pip installs needed)
- OpenCode installed and authenticated
