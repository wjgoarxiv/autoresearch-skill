#!/usr/bin/env bash
# release.sh — Bump version, tag, and prepare changelog for autoresearch-skill
#
# Usage:
#   bash scripts/release.sh 2.0.0
#   bash scripts/release.sh 2.1.0 "Add new subcommand"

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION="${1:-}"
MESSAGE="${2:-}"

if [[ -z "$VERSION" ]]; then
  echo "Usage: bash scripts/release.sh <version> [message]"
  echo "  e.g: bash scripts/release.sh 2.0.0"
  exit 1
fi

if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Error: version must be semver (e.g. 2.0.0)"
  exit 1
fi

echo "Releasing autoresearch-skill v${VERSION}..."

# 1. Update .claude-plugin/plugin.json
PLUGIN_JSON="${REPO_ROOT}/.claude-plugin/plugin.json"
if [[ -f "$PLUGIN_JSON" ]]; then
  python3 -c "
import json, sys
with open('${PLUGIN_JSON}') as f:
    d = json.load(f)
d['version'] = '${VERSION}'
with open('${PLUGIN_JSON}', 'w') as f:
    json.dump(d, f, indent=2)
    f.write('\n')
print('Updated ${PLUGIN_JSON}')
"
fi

# 2. Update .claude-plugin/marketplace.json
MARKET_JSON="${REPO_ROOT}/.claude-plugin/marketplace.json"
if [[ -f "$MARKET_JSON" ]]; then
  python3 -c "
import json, sys
with open('${MARKET_JSON}') as f:
    d = json.load(f)
d['version'] = '${VERSION}'
with open('${MARKET_JSON}', 'w') as f:
    json.dump(d, f, indent=2)
    f.write('\n')
print('Updated ${MARKET_JSON}')
"
fi

# 3. Update root SKILL.md frontmatter version comment (if present)
# The frontmatter doesn't have a version field but we can add/update a comment
SKILL_MD="${REPO_ROOT}/SKILL.md"
if grep -q "^# autoresearch-skill v" "$SKILL_MD" 2>/dev/null; then
  sed -i.bak "s/^# autoresearch-skill v[0-9.]*/# autoresearch-skill v${VERSION}/" "$SKILL_MD"
  rm -f "${SKILL_MD}.bak"
  echo "Updated ${SKILL_MD}"
fi

# 4. Stage version-bumped files
cd "$REPO_ROOT"
git add .claude-plugin/plugin.json .claude-plugin/marketplace.json 2>/dev/null || true

# 5. Create git commit
COMMIT_MSG="${MESSAGE:-Release v${VERSION}}"
git diff --cached --quiet || git commit -m "chore(release): v${VERSION} — ${COMMIT_MSG}"

# 6. Create annotated git tag
if git tag -l | grep -q "^v${VERSION}$"; then
  echo "Warning: tag v${VERSION} already exists — skipping tag creation"
else
  git tag -a "v${VERSION}" -m "autoresearch-skill v${VERSION}"
  echo "Created tag: v${VERSION}"
fi

echo ""
echo "Release v${VERSION} prepared."
echo ""
echo "Next steps:"
echo "  git push origin main"
echo "  git push origin v${VERSION}"
echo ""
echo "Then update the GitHub release notes at:"
echo "  https://github.com/wjgoarxiv/autoresearch-skill/releases/new?tag=v${VERSION}"
