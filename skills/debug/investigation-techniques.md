# Investigation Techniques

Seven systematic techniques for debugging. Each targets a different layer of the system. When one technique stops producing new evidence, switch to another.

---

## 1. Bisect — Binary Search Over Commits or Config

**When to use:** The bug was not present in an older state (commit, config, dataset). You know a "good" state and a "bad" state but not the change that introduced the regression.

**How to apply:**
1. Identify the good state (last known working commit/config) and bad state (current failing state).
2. Pick the midpoint between them.
3. Test the midpoint — does the bug appear?
4. If yes: the regression is in the first half. If no: the regression is in the second half.
5. Repeat, halving the search space each iteration. Converges in O(log N) steps.

**What output to expect:** A single commit, config line, or dataset entry that introduces the failure. That change is the root cause candidate.

**Example commands:**
```bash
# Git bisect (automated)
git bisect start
git bisect bad HEAD
git bisect good v1.2.0
git bisect run python test_reproducer.py
git bisect reset

# Manual bisect over a config array
# Test config[0..N/2], then narrow based on result
```

---

## 2. strace / dtrace — System Call Tracing

**When to use:** The bug manifests at the OS level — file not found, permission denied, network timeout, unexpected signal. User-space logging is insufficient. You need to see what the process is actually asking the kernel to do.

**How to apply:**
1. Attach strace (Linux) or dtrace (macOS) to the failing process.
2. Filter to the relevant system call family (file I/O, network, signals).
3. Run the reproduction case.
4. Search the trace for unexpected calls, errors (ENOENT, EACCES, ETIMEDOUT), or missing calls.

**What output to expect:** A stream of system calls with arguments and return values. Look for the first call that returns an unexpected error code.

**Example commands:**
```bash
# Linux: trace file and network calls
strace -e trace=file,network -f python reproduce.py 2>&1 | grep -E "ENOENT|EACCES|ERROR"

# Linux: trace a running process by PID
strace -p PID -e trace=file,network

# macOS: trace file opens
sudo dtrace -n 'syscall::open*:entry { printf("%s %s", execname, copyinstr(arg0)); }' 2>/dev/null

# macOS: trace network connect calls
sudo dtrace -n 'syscall::connect:entry { printf("%s", execname); }' 2>/dev/null
```

---

## 3. Flamegraph — CPU and Memory Profiling

**When to use:** Performance regression — the code is correct but slow, uses too much memory, or spends time in unexpected places. The bug is not an error but a resource usage anomaly.

**How to apply:**
1. Profile the failing execution (sampling profiler captures call stacks at intervals).
2. Aggregate stacks into a flamegraph.
3. Identify the widest bars — those are where wall-clock time is spent.
4. Compare the flamegraph of the slow case to the fast (baseline) case.
5. Look for functions that appear in the slow flamegraph but not the fast one, or that are proportionally wider.

**What output to expect:** A flamegraph SVG. The root cause of a performance bug appears as a wide unexpected bar. Before/after comparison reveals the regression.

**Example commands:**
```bash
# Python: generate a flamegraph with py-spy
pip install py-spy
py-spy record -o flamegraph.svg -- python slow_script.py

# Python: cProfile for a quick call breakdown
python -m cProfile -s cumtime slow_script.py | head -30

# Node.js
node --prof app.js && node --prof-process isolate-*.log > profile.txt

# Comparison: run both baseline and current, diff the top-N functions
python -m cProfile -o baseline.prof baseline.py
python -m cProfile -o current.prof current.py
python -c "import pstats; p=pstats.Stats('current.prof'); p.sort_stats('cumtime'); p.print_stats(20)"
```

---

## 4. Hypothesis Testing — Statistical Verification

**When to use:** The bug is intermittent, or the metric difference between working and broken is small enough to be noise. You need to determine whether the observed difference is real or random.

**How to apply:**
1. Define the null hypothesis: "There is no difference between condition A and condition B."
2. Collect N samples from each condition (N >= 30 for reliable results, more for high variance).
3. Run a statistical test appropriate to the data distribution.
4. If p-value < 0.05, the difference is statistically significant — the null hypothesis is rejected.
5. Report the effect size (not just p-value) to understand if the difference is practically meaningful.

**What output to expect:** A p-value and confidence interval. p < 0.05 means the effect is real, not noise. Effect size tells you how large it is.

**Example commands:**
```bash
# Python: t-test for two independent samples
python3 -c "
import scipy.stats as stats
import numpy as np
baseline = [0.91, 0.89, 0.92, 0.88, 0.90]  # replace with real data
current  = [0.85, 0.84, 0.86, 0.83, 0.85]
t, p = stats.ttest_ind(baseline, current)
print(f't={t:.3f}  p={p:.4f}  significant={p<0.05}')
print(f'baseline mean={np.mean(baseline):.3f}  current mean={np.mean(current):.3f}')
"

# Collect N samples of a metric for statistical comparison
for i in $(seq 1 30); do python benchmark.py >> samples.txt; done
```

---

## 5. Differential Diagnosis — Compare Working vs Broken

**When to use:** You have two environments, versions, inputs, or configurations — one that works and one that does not. The difference between them is the root cause.

**How to apply:**
1. Identify the minimal pair: one working state, one broken state, as similar as possible in every other dimension.
2. List all known differences between them (environment variables, library versions, config values, data shape).
3. Systematically transfer each difference from the working state to the broken state (or vice versa), one at a time.
4. The transfer that fixes (or causes) the bug identifies the root cause.

**What output to expect:** A specific difference — a library version, a config key, a data characteristic — that is the root cause. When you change only that one thing, the behavior changes.

**Example commands:**
```bash
# Compare environment variables
diff <(env | sort) <(ssh remote-host env | sort)

# Compare installed package versions
pip freeze > current_env.txt
diff baseline_env.txt current_env.txt

# Compare config files
diff working_config.yaml broken_config.yaml

# Compare file checksums between two directories
diff <(find working_dir -type f | xargs md5sum | sort) \
     <(find broken_dir  -type f | xargs md5sum | sort)

# Compare library versions explicitly
python -c "import pkg; print(pkg.__version__)"
```

---

## 6. Minimal Reproduction — Smallest Failing Case

**When to use:** The bug is confirmed but the reproduction case is complex (large codebase, large dataset, long setup). A complex reproduction case makes it hard to reason about root cause. Shrinking it isolates the essential condition.

**How to apply:**
1. Start with the full reproduction case.
2. Remove one component (a function call, a data field, a config option, a dependency).
3. Does the bug still occur? If yes, the removed component is not necessary — keep it removed.
4. Repeat until nothing more can be removed without making the bug disappear.
5. The result is the minimal reproduction case.

**What output to expect:** A standalone script, config, or input of 10-50 lines that reliably triggers the bug. The essential condition causing the bug is visible in this minimal case.

**Example commands:**
```bash
# Bisect a large input file down to minimal failing input
# Start: wc -l input.txt -> 10000 lines
head -5000 input.txt > test_input.txt && python reproduce.py test_input.txt
# If still fails: head -2500 ...
# If passes: tail -5000 ... (the bug is in the second half)
# Converge to the minimal failing subset

# Shrink a test case programmatically
# Remove imports one by one, run after each removal
# Remove function calls one by one, run after each removal

# Check if bug reproduces in isolation
python -c "
# Paste only the suspected function here
# Call it with the suspected input
# See if the bug reproduces without the rest of the codebase
"
```

---

## 7. Instrumentation — Adding Logging and Metrics

**When to use:** The bug is inside a running system where you cannot pause execution or attach a debugger. You need to observe internal state without stopping the system. Also useful when the bug is a race condition or timing-sensitive.

**How to apply:**
1. Identify the code path you suspect is the root cause.
2. Add logging statements that emit: timestamp, thread/process ID, variable values, control flow markers.
3. Add counters or gauges for quantities you want to track over time (queue depth, connection count, cache hit rate).
4. Re-run the reproduction case with instrumentation active.
5. Read the logs: look for the moment the internal state diverges from expected.
6. Remove all instrumentation after the root cause is found.

**What output to expect:** A log stream showing the exact sequence of internal state changes that leads to the failure. The root cause is the first state transition that should not have occurred.

**Example commands:**
```python
# Python: structured logging with timestamps
import logging, time
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

# Add at suspected entry point:
log.debug("enter process_request state=%s queue_depth=%d", state, len(queue))

# Add before suspected failure point:
log.debug("pre-write cache_key=%s ttl=%d", key, ttl)
```

```bash
# Trace every function call in a Python script (without modifying source)
python -m trace --trace suspect_module.py 2>&1 | grep "suspect_module.py"

# Add timing probes with bash
time_start=$(date +%s%N)
# ... operation ...
time_end=$(date +%s%N)
echo "elapsed: $(( (time_end - time_start) / 1000000 ))ms"

# Count occurrences of a log pattern in real time
tail -f app.log | grep --line-buffered "ERROR" | awk '{count++; print count, $0}'
```

---

## Technique Selection Guide

| Symptom | First technique | If stuck, try |
|---------|----------------|---------------|
| "Was working before commit X" | bisect | differential diagnosis |
| "Only fails in production, not dev" | differential diagnosis | strace/dtrace |
| "Slow, not wrong" | flamegraph | hypothesis testing |
| "Sometimes fails" | hypothesis testing | instrumentation |
| "Error deep in a library" | minimal reproduction | strace/dtrace |
| "Hard to reproduce" | minimal reproduction | instrumentation |
| "Fails at OS level (file/network)" | strace/dtrace | differential diagnosis |
| "Need to see internal state" | instrumentation | flamegraph |
