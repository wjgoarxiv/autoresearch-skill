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
4-frequency Fourier model with frequencies 1/sqrt(2), sqrt(2), 3.04, 7.0. Current RMSE: 0.0344.

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
| 1 | 4-freq Fourier (0.8, 1.38, 3.05, 7.0) | 0.0349 | improved | 2026-03-29 |
| 2 | 6-freq Fourier (added 4.3, 5.0) | 0.0392 | reverted | 2026-03-29 |
| 3 | Refined 4-freq (0.75, 1.34, 3.04, 7.02) | 0.0368 | reverted | 2026-03-29 |
| 4 | Alt freq set (0.5, 2.96, 6.96, 2.8) | 0.0485 | reverted | 2026-03-29 |
| 5 | Gradient-optimized params | 0.0349 | no improvement | 2026-03-29 |
| 6 | Analytical: sin(3x)+cos(7x) deep analysis | -- | analysis only | 2026-03-29 |
| 7 | CV-optimized freqs (0.7, 1.38, 3.04, 7.0) | 0.0345 | improved | 2026-03-29 |
| 8 | Fourier + product terms | 0.0372 | reverted | 2026-03-29 |
| 9 | Alt freq (0.5, 2.0, 3.04, 7.0) | 0.0360 | reverted | 2026-03-29 |
| 10 | LOOCV-optimized (0.5, 1.83, 3.04, 7.01) | 0.0366 | reverted | 2026-03-29 |
| 11 | Quadratic envelope + sin(3x) + cos(7x) | 0.0519 | reverted | 2026-03-29 |
| 12 | Coordinate-descent refined | 0.0359 | reverted | 2026-03-29 |
| 13 | 5-freq (added w5=4.3) | 0.0361 | reverted | 2026-03-29 |
| 14 | Rounded/simplified coefficients | 0.0360 | reverted | 2026-03-29 |
| 15 | Ridge regression (lambda=0.02) | 0.0347 | reverted | 2026-03-29 |
| 16 | 1/sqrt(2), sqrt(2), 3.04, 7.0 | 0.0344 | improved | 2026-03-29 |
| 17 | Fine-tuned w3=3.037, w4=7.014 | 0.0358 | reverted | 2026-03-29 |
| 18 | w4=7.01 variant | 0.0355 | reverted | 2026-03-29 |
