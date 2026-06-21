"""Lightweight repository validation for autoresearch-skill.

Stdlib-only checks for required metadata, templates, documentation links,
and eval coverage.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse


REPO_ROOT = Path(__file__).resolve().parents[1]

JSON_FILES = [
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    "context7.json",
    "evals/evals.json",
]

REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "assets/research_template.md",
    "assets/results_template.tsv",
    "scripts/init_research.py",
    "skills/autoresearch/SKILL.md",
]

EXPECTED_TSV_HEADER = [
    "iteration",
    "metric_value",
    "delta",
    "delta_pct",
    "status",
    "description",
    "evaluator_source",
    "timestamp",
]

MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HTML_LINK_RE = re.compile(r"\b(?:src|href)\s*=\s*([\"'])(.*?)\1", re.IGNORECASE)
REQUIRED_README_SNIPPETS = [
    "Expected Outputs: Visual Result Gallery",
    "./examples/code-optimization/results.png",
    "./examples/function-fitting/results.png",
    "autoresearch-results.tsv",
    "progress.png",
    "final_report.md",
]
REQUIRED_EVAL_COMMANDS = [
    "/autoresearch:plan",
    "/autoresearch:debug",
    "/autoresearch:fix",
    "/autoresearch:predict",
    "/autoresearch:security",
    "/autoresearch:scenario",
    "/autoresearch:reason",
    "/autoresearch:ship",
    "/autoresearch:learn",
]


def _relative(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _strip_markdown_target(raw_target: str) -> str:
    target = raw_target.strip()
    if not target:
        return ""
    if target[0] in "'\"":
        quote = target[0]
        end = target.find(quote, 1)
        if end != -1:
            return target[1:end]
    return target.split()[0]


def _is_ignored_reference(target: str) -> bool:
    if not target or target.startswith("#"):
        return True
    parsed = urlparse(target)
    if parsed.scheme in {"http", "https", "mailto"}:
        return True
    return False


def check_json(files):
    errors = []
    for rel_path in JSON_FILES:
        path = REPO_ROOT / rel_path
        if not path.exists():
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON in {rel_path}: {exc.msg} at line {exc.lineno}, column {exc.colno}")
    return errors


def check_required_files(files):
    errors = []
    for rel_path in REQUIRED_FILES:
        if not (REPO_ROOT / rel_path).is_file():
            errors.append(f"Missing required file: {rel_path}")
    return errors


def check_results_template(files):
    path = REPO_ROOT / "assets/results_template.tsv"
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    first_line = lines[0] if lines else ""
    header = first_line.split("\t") if first_line else []
    if header != EXPECTED_TSV_HEADER:
        return [
            "assets/results_template.tsv header mismatch: "
            f"expected {EXPECTED_TSV_HEADER!r}, got {header!r}"
        ]
    return []


def _local_reference_path(target: str):
    parsed = urlparse(target)
    path_part = unquote(parsed.path)
    if not path_part:
        return None
    return path_part


def check_readme_links(files):
    readme = REPO_ROOT / "README.md"
    if not readme.exists():
        return []

    errors = []
    for line_no, line in enumerate(readme.read_text(encoding="utf-8").splitlines(), start=1):
        targets = [_strip_markdown_target(match.group(1)) for match in MARKDOWN_LINK_RE.finditer(line)]
        targets.extend(match.group(2).strip() for match in HTML_LINK_RE.finditer(line))
        for target in targets:
            if _is_ignored_reference(target):
                continue
            local_ref = _local_reference_path(target)
            if not local_ref:
                continue
            candidate = (readme.parent / local_ref).resolve()
            try:
                candidate.relative_to(REPO_ROOT)
            except ValueError:
                errors.append(f"README.md:{line_no}: local reference escapes repo: {target}")
                continue
            if not candidate.exists():
                errors.append(f"README.md:{line_no}: missing local reference: {target}")
    return errors


def check_readme_expected_outputs(files):
    readme = REPO_ROOT / "README.md"
    if not readme.exists():
        return []
    text = readme.read_text(encoding="utf-8")
    missing = [snippet for snippet in REQUIRED_README_SNIPPETS if snippet not in text]
    if missing:
        return ["README.md missing expected output showcase snippet(s): " + ", ".join(missing)]
    return []


def _frontmatter_fields(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fields = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip()
    return fields


def check_skill_frontmatter(files):
    errors = []
    skill_files = [REPO_ROOT / "SKILL.md"] + sorted((REPO_ROOT / "skills").glob("*/SKILL.md"))
    for path in skill_files:
        if not path.exists():
            continue
        fields = _frontmatter_fields(path)
        missing = [field for field in ("name", "description") if field not in fields]
        if missing:
            errors.append(f"{_relative(path)} missing frontmatter field(s): {', '.join(missing)}")
    return errors


def load_evals():
    path = REPO_ROOT / "evals/evals.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def check_evals(files):
    path = REPO_ROOT / "evals/evals.json"
    if not path.exists():
        return []

    errors = []
    try:
        data = load_evals()
    except json.JSONDecodeError as exc:
        return [f"Invalid JSON in evals/evals.json: {exc.msg} at line {exc.lineno}, column {exc.colno}"]

    if not data.get("skill_name"):
        errors.append("evals/evals.json missing non-empty skill_name")
    evals = data.get("evals")
    if not isinstance(evals, list) or not evals:
        errors.append("evals/evals.json missing non-empty evals list")
        return errors

    required = ("id", "prompt", "expected_output")
    for index, entry in enumerate(evals, start=1):
        if not isinstance(entry, dict):
            errors.append(f"evals/evals.json eval #{index} must be an object")
            continue
        missing = [field for field in required if field not in entry or entry[field] in ("", None)]
        if missing:
            errors.append(f"evals/evals.json eval #{index} missing field(s): {', '.join(missing)}")
    return errors


def check_eval_coverage(files):
    try:
        data = load_evals()
    except json.JSONDecodeError as exc:
        return [f"Invalid JSON in evals/evals.json: {exc.msg} at line {exc.lineno}, column {exc.colno}"]
    if not data:
        return ["evals/evals.json not present"]
    corpus = "\n".join(
        f"{entry.get('prompt', '')}\n{entry.get('expected_output', '')}"
        for entry in data.get("evals", [])
        if isinstance(entry, dict)
    )
    missing = [command for command in REQUIRED_EVAL_COMMANDS if command not in corpus]
    if missing:
        return ["evals/evals.json missing subcommand coverage for: " + ", ".join(missing)]
    return []


def eval_summary():
    data = load_evals()
    if not data:
        return "Eval coverage: evals/evals.json not present"
    evals = data.get("evals") or []
    ids = [str(entry.get("id", "<missing>")) for entry in evals if isinstance(entry, dict)]
    return f"Eval coverage: {len(evals)} eval(s) for {data.get('skill_name', '<missing>')}; ids: {', '.join(ids)}"


def run_validation(include_eval_coverage=False):
    checks = [
        check_json,
        check_required_files,
        check_results_template,
        check_readme_links,
        check_readme_expected_outputs,
        check_skill_frontmatter,
        check_evals,
    ]
    if include_eval_coverage:
        checks.append(check_eval_coverage)
    errors = []
    for check in checks:
        errors.extend(check(None))
    return errors


def parse_args():
    parser = argparse.ArgumentParser(description="Validate autoresearch-skill repository metadata.")
    parser.add_argument("--evals", action="store_true", help="include eval coverage summary after validation")
    return parser.parse_args()


def main():
    args = parse_args()
    errors = run_validation(include_eval_coverage=args.evals)
    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Validation passed")
    if args.evals:
        print(eval_summary())
    return 0


if __name__ == "__main__":
    sys.exit(main())
