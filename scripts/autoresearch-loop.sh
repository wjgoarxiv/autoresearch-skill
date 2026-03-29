#!/usr/bin/env bash
# autoresearch-loop.sh — Universal overnight autoresearch outer-loop runner
#
# Detects the active AI CLI tool, then repeatedly invokes it with a
# continuation prompt until the research completes or max invocations
# is reached. Checks file-based completion signals before each call.
#
# Usage:
#   autoresearch-loop.sh [OPTIONS] <research_dir>
#
# Options:
#   --cli <name>              Override CLI auto-detection (claude|codex|opencode|gemini)
#   --interval <seconds>      Wait time between invocations (default: 360)
#   --max-invocations <N>     Maximum number of CLI invocations (default: 50)
#   --dry-run                 Print commands without executing them
#   -h, --help                Show this help message

set -euo pipefail

# ─── Constants ────────────────────────────────────────────────────────────────

readonly SCRIPT_NAME="autoresearch-loop"
readonly DEFAULT_INTERVAL=360
readonly DEFAULT_MAX_INVOCATIONS=50
readonly PID_FILE_NAME=".autoresearch-loop.pid"

# Continuation prompt sent to the CLI on every invocation
readonly CONTINUATION_PROMPT="Continue the autoresearch loop in this directory. Read research.md and research_log.md. Resume from the last completed iteration. Run as many iterations as possible within this session. Follow the Autonomy Directive: do not pause, do not ask for confirmation, do not stop until the target is met or max_iterations is exhausted."

# ─── Defaults ─────────────────────────────────────────────────────────────────

cli_override=""
interval=$DEFAULT_INTERVAL
max_invocations=$DEFAULT_MAX_INVOCATIONS
dry_run=false
research_dir=""

# ─── Helpers ──────────────────────────────────────────────────────────────────

usage() {
    sed -n '/^# Usage:/,/^$/p' "$0" | sed 's/^# \{0,2\}//'
    exit 0
}

log() {
    # Timestamped log line to stdout
    printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"
}

die() {
    printf 'ERROR: %s\n' "$*" >&2
    exit 1
}

# ─── Argument parsing ─────────────────────────────────────────────────────────

while [[ $# -gt 0 ]]; do
    case "$1" in
        --cli)
            [[ $# -ge 2 ]] || die "--cli requires an argument"
            cli_override="$2"
            shift 2
            ;;
        --interval)
            [[ $# -ge 2 ]] || die "--interval requires an argument"
            interval="$2"
            shift 2
            ;;
        --max-invocations)
            [[ $# -ge 2 ]] || die "--max-invocations requires an argument"
            max_invocations="$2"
            shift 2
            ;;
        --dry-run)
            dry_run=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        -*)
            die "Unknown option: $1"
            ;;
        *)
            # First non-option argument is the research directory
            research_dir="$1"
            shift
            ;;
    esac
done

# ─── Validate inputs ──────────────────────────────────────────────────────────

[[ -n "$research_dir" ]] || die "research_dir is required as the first positional argument"
[[ -d "$research_dir" ]] || die "research_dir does not exist or is not a directory: $research_dir"
[[ -f "${research_dir}/research.md" ]] || die "No research.md found in ${research_dir}. Run init_research.py first."

# Resolve to absolute path
research_dir="$(cd "$research_dir" && pwd)"

# Validate numeric args
[[ "$interval" =~ ^[0-9]+$ ]]         || die "--interval must be a positive integer"
[[ "$max_invocations" =~ ^[0-9]+$ ]]  || die "--max-invocations must be a positive integer"

# ─── CLI detection ────────────────────────────────────────────────────────────

detect_cli() {
    for candidate in claude codex opencode gemini; do
        if command -v "$candidate" &>/dev/null; then
            printf '%s' "$candidate"
            return 0
        fi
    done
    return 1
}

if [[ -n "$cli_override" ]]; then
    cli="$cli_override"
    command -v "$cli" &>/dev/null || die "Specified CLI '$cli' not found in PATH"
else
    cli="$(detect_cli)" || die "No supported AI CLI found. Install claude, codex, opencode, or gemini."
fi

# ─── PID management ───────────────────────────────────────────────────────────

pid_file="${research_dir}/${PID_FILE_NAME}"

cleanup() {
    rm -f "$pid_file"
}
trap cleanup EXIT INT TERM

printf '%d\n' "$$" > "$pid_file"

# ─── Build the CLI invocation command ────────────────────────────────────────

# Returns the full command as an array in the global variable CMD_ARRAY.
# Callers must eval or use "${CMD_ARRAY[@]}".
build_cmd() {
    CMD_ARRAY=()
    case "$cli" in
        claude)
            # claude supports -C for working directory
            CMD_ARRAY=(claude -C "$research_dir" -p "$CONTINUATION_PROMPT" --permission-mode auto)
            ;;
        codex)
            # codex supports -C for working directory
            CMD_ARRAY=(codex -C "$research_dir" exec "$CONTINUATION_PROMPT" --full-auto)
            ;;
        opencode)
            # opencode uses --dir for working directory
            CMD_ARRAY=(opencode run "$CONTINUATION_PROMPT" --dir "$research_dir")
            ;;
        gemini)
            # gemini has no cwd flag; we cd before invoking
            CMD_ARRAY=(bash -c "cd $(printf '%q' "$research_dir") && gemini -p $(printf '%q' "$CONTINUATION_PROMPT") -y")
            ;;
        *)
            die "Unsupported CLI: $cli"
            ;;
    esac
}

# ─── Completion detection ─────────────────────────────────────────────────────

# Returns 0 (true) if research is complete, 1 (false) otherwise.
is_complete() {
    local dir="$1"

    # 1. final_report.md exists → done
    if [[ -f "${dir}/final_report.md" ]]; then
        log "Completion detected: final_report.md found."
        return 0
    fi

    # 2. Check iteration count against max_iterations from research.md
    local research_md="${dir}/research.md"
    local results_tsv="${dir}/autoresearch-results.tsv"
    if [[ -f "$research_md" && -f "$results_tsv" ]]; then
        # Extract "Max iterations:** <N>" — handles bold markdown or plain text
        local max_iters
        max_iters="$(grep -i 'max.iterations' "$research_md" \
                     | grep -oE '[0-9]+' \
                     | head -1)" || true
        if [[ -n "$max_iters" && "$max_iters" -gt 0 ]]; then
            # Last row, first column (iteration index, 0-based)
            local last_iter
            last_iter="$(tail -1 "$results_tsv" | cut -f1)" || true
            if [[ "$last_iter" =~ ^[0-9]+$ ]]; then
                local threshold=$(( max_iters - 1 ))
                if [[ "$last_iter" -ge "$threshold" ]]; then
                    log "Completion detected: last iteration ${last_iter} >= max_iterations-1 (${threshold})."
                    return 0
                fi
            fi
        fi
    fi

    # 3. research.md contains "target.*achieved" or "target.*met" (case-insensitive)
    if [[ -f "$research_md" ]]; then
        if grep -qiE 'target.*(achieved|met)' "$research_md"; then
            log "Completion detected: target achieved/met phrase found in research.md."
            return 0
        fi
    fi

    return 1
}

# ─── Header ───────────────────────────────────────────────────────────────────

print_header() {
    printf '\n'
    printf '═══════════════════════════════════════════════════\n'
    printf '  autoresearch-loop — Universal overnight runner\n'
    printf '  CLI:         %s\n' "$cli"
    printf '  Research:    %s\n' "$research_dir"
    printf '  Interval:    %ss\n' "$interval"
    printf '  Max invokes: %s\n' "$max_invocations"
    printf '═══════════════════════════════════════════════════\n'
    printf '\n'
}

# ─── Main loop ────────────────────────────────────────────────────────────────

print_header

invocation=0
exit_reason="max_invocations reached"

while [[ $invocation -lt $max_invocations ]]; do

    # Check completion before invoking
    if is_complete "$research_dir"; then
        exit_reason="completion detected before invocation $((invocation + 1))"
        break
    fi

    invocation=$(( invocation + 1 ))
    log "Invocation ${invocation}/${max_invocations} starting."

    build_cmd

    if $dry_run; then
        log "[DRY-RUN] Would execute: ${CMD_ARRAY[*]}"
    else
        # Execute and allow non-zero exit (the AI CLI may return non-zero on normal exit)
        "${CMD_ARRAY[@]}" || log "CLI exited with non-zero status (continuing loop)."
    fi

    log "Invocation ${invocation}/${max_invocations} finished."

    # Check completion after this invocation
    if is_complete "$research_dir"; then
        exit_reason="completion detected after invocation ${invocation}"
        break
    fi

    # Wait before next invocation (skip after the last one)
    if [[ $invocation -lt $max_invocations ]]; then
        log "Waiting ${interval}s before next invocation..."
        sleep "$interval"
    fi

done

# ─── Summary ──────────────────────────────────────────────────────────────────

printf '\n'
printf '═══════════════════════════════════════════════════\n'
printf '  autoresearch-loop complete\n'
printf '  Invocations run: %s\n' "$invocation"
printf '  Exit reason:     %s\n' "$exit_reason"
printf '  Research dir:    %s\n' "$research_dir"
printf '═══════════════════════════════════════════════════\n'
printf '\n'
