#!/usr/bin/env bash
# check_progress.sh - Lightweight progress monitor for autoresearch runs
# Usage: check_progress.sh [research_dir]

RESEARCH_DIR="${1:-.}"
RESEARCH_DIR="${RESEARCH_DIR%/}"  # strip trailing slash

RESEARCH_MD="$RESEARCH_DIR/research.md"
TSV_FILE="$RESEARCH_DIR/autoresearch-results.tsv"
FINAL_REPORT="$RESEARCH_DIR/final_report.md"
PID_FILE="$RESEARCH_DIR/.autoresearch-loop.pid"

# ── Parse research.md ────────────────────────────────────────────────────────

if [[ -f "$RESEARCH_MD" ]]; then
    max_iter=$(grep -m1 '\*\*Max iterations:\*\*' "$RESEARCH_MD" \
               | sed 's/.*\*\*Max iterations:\*\*[[:space:]]*//' \
               | awk '{print $1}')
    target=$(grep -m1 '\*\*Target:\*\*' "$RESEARCH_MD" \
             | sed 's/.*\*\*Target:\*\*[[:space:]]*//' \
             | sed 's/[[:space:]]*$//')
    direction=$(grep -m1 '\*\*Direction:\*\*' "$RESEARCH_MD" \
                | sed 's/.*\*\*Direction:\*\*[[:space:]]*//' \
                | awk '{print $1}')
    metric=$(grep -m1 '\*\*Metric:\*\*' "$RESEARCH_MD" \
             | sed 's/.*\*\*Metric:\*\*[[:space:]]*//' \
             | sed 's/[[:space:]]*$//')
    # First non-empty line after "## Goal"
    goal=$(awk '/^## Goal/{found=1; next} found && /[^[:space:]]/{print; exit}' \
           "$RESEARCH_MD")
else
    max_iter="?"; target="?"; direction="?"; metric="?"; goal="?"
fi

[[ -z "$max_iter"  ]] && max_iter="?"
[[ -z "$target"    ]] && target="?"
[[ -z "$direction" ]] && direction="?"
[[ -z "$metric"    ]] && metric="?"
[[ -z "$goal"      ]] && goal="?"

# ── Parse autoresearch-results.tsv ───────────────────────────────────────────

cur_iter="?"; best_score="?"; last_status="?"; last_desc="?"

if [[ -f "$TSV_FILE" ]]; then
    # Skip header row (first line), collect data lines portably (bash 3.2 safe)
    data_count=0
    best_score=""
    while IFS=$'\t' read -r f1 f2 f3 f4 f5 f6 f7 rest; do
        [[ -z "$f1" ]] && continue
        data_count=$(( data_count + 1 ))
        cur_iter="$f1"
        last_status="$f5"
        last_desc="$f6"
        val="$f2"
        # Track best score; skip non-numeric values (e.g. "-")
        if [[ "$val" =~ ^-?[0-9]+(\.[0-9]+)?$ ]]; then
            if [[ -z "$best_score" ]]; then
                best_score="$val"
            else
                if [[ "$direction" == "minimize" ]]; then
                    better=$(awk -v a="$val" -v b="$best_score" 'BEGIN{print (a<b)?1:0}')
                else
                    better=$(awk -v a="$val" -v b="$best_score" 'BEGIN{print (a>b)?1:0}')
                fi
                [[ "$better" == "1" ]] && best_score="$val"
            fi
        fi
    done < <(tail -n +2 "$TSV_FILE" | grep -v '^[[:space:]]*$')

    [[ -z "$best_score" ]] && best_score="?"
fi

# ── Determine run status ──────────────────────────────────────────────────────

if [[ -f "$FINAL_REPORT" ]]; then
    run_status="COMPLETE"
elif [[ -f "$TSV_FILE" ]] && [[ "${data_count:-0}" -gt 0 ]]; then
    run_status="running"
else
    run_status="no data"
fi

if [[ -f "$PID_FILE" ]]; then
    pid=$(cat "$PID_FILE" 2>/dev/null)
    if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
        run_status="$run_status (loop active)"
    fi
fi

# ── Build display strings ─────────────────────────────────────────────────────

iter_display="$cur_iter / ${max_iter}"
target_display="$target ($direction)"

# Truncate long strings to keep box tidy (max ~44 chars for value column)
_trunc() {
    local s="$1" max="${2:-44}"
    if [[ ${#s} -gt $max ]]; then
        printf '%s…' "${s:0:$((max-1))}"
    else
        printf '%s' "$s"
    fi
}

label_w=12   # width of label column including trailing spaces
val_w=44     # max width of value column

research_val=$(_trunc "$RESEARCH_DIR/" $val_w)
goal_val=$(_trunc "$goal" $val_w)
iter_val=$(_trunc "$iter_display" $val_w)
score_val=$(_trunc "$best_score" $val_w)
target_val=$(_trunc "$target_display" $val_w)
status_val=$(_trunc "$run_status" $val_w)
last_val=$(_trunc "$last_desc" $val_w)

# ── Box drawing ───────────────────────────────────────────────────────────────

# Compute box inner width from widest row
_row_len() { printf '%s' "  ${1}${2}" | wc -c | tr -d ' '; }

inner_w=54  # fixed inner width for clean alignment
border=$(printf '─%.0s' $(seq 1 $inner_w))

_pad_row() {
    local label="$1" value="$2"
    local content="  ${label}${value}"
    local pad=$(( inner_w - ${#content} ))
    if [[ $pad -lt 0 ]]; then
        # truncate value
        local max_val=$(( inner_w - ${#label} - 2 ))
        value="${value:0:$((max_val-1))}…"
        content="  ${label}${value}"
        pad=0
    fi
    printf '│%s%*s│\n' "$content" "$pad" ""
}

printf '┌─ autoresearch progress ─%s┐\n' "$(printf '─%.0s' $(seq 1 $((inner_w - 26))))"
_pad_row "Research:   " "$research_val"
_pad_row "Goal:       " "$goal_val"
_pad_row "Iteration:  " "$iter_val"
_pad_row "Best score: " "$score_val"
_pad_row "Target:     " "$target_val"
_pad_row "Status:     " "$status_val"
_pad_row "Last:       " "$last_val"
printf '└%s┘\n' "$border"
