# Research: Discover Hidden Mathematical Function via Iterative Fitting

## Goal
Discover the underlying mathematical function that generated the data in `train_data.csv` and `test_data.csv`. The data contains 80 training points and 40 test points of (x, y) pairs sampled from an unknown composite function with small Gaussian noise (std ~0.03). The x range is [-3, 3].

Modify `predict.py` so that `predict(x)` approximates the true function as closely as possible, minimizing RMSE on the test set to below 0.05.

## Success Metric
- **Metric:** RMSE (Root Mean Squared Error) on test_data.csv
- **Target:** < 0.05
- **Direction:** minimize

## Constraints
- **Max iterations:** 25
- **Time budget per experiment:** 2 minutes
- **Pause for review every:** never
- **Evaluator:** `python evaluate.py`
- **Keep policy:** score_improvement

## Current Approach
Naive linear approximation: `predict(x) = x`. Current RMSE: ~2.11.

## Search Space
- **Allowed changes:** The `predict(x)` function body in `predict.py`. Any Python math operations using the `math` standard library module. Polynomial terms, trigonometric functions, exponential functions, piecewise functions, or combinations thereof.
- **Forbidden changes:** `evaluate.py`, `generate_data.py`, `train_data.csv`, `test_data.csv`. Do NOT read `generate_data.py` to discover the hidden function — that is cheating.

## Context & References
- The data appears to have oscillatory patterns (visible if you plot train_data.csv)
- The function likely has multiple frequency components
- Standard approaches: polynomial regression, Fourier series, basis function expansion
- You may read `train_data.csv` to analyze patterns, but NOT `generate_data.py`
- Use `math` module only (no numpy/scipy in predict.py to keep it portable)
- You CAN use numpy in scratch analysis scripts, but `predict.py` must use only `math`

---

## History
<!-- Auto-maintained by the agent. Do not edit manually. -->
| # | Change | Metric (RMSE) | Result | Timestamp |
|---|--------|---------------|--------|-----------|
| 0 | Baseline: predict(x) = x | 2.11 | -- | 2026-03-29 |
