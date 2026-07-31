# Task Instructions & Pinned Conventions

## Pinned curve_fit Convention
Justification for `no-sigma`: While `absolute_sigma=True` is physically correct for known measurement error, it scales the covariance matrix (`pcov`) by the reduced chi-square based on the exact fit residuals. This breaks reproducibility across identical solver fits due to floating-point differences. The pinned `no-sigma` convention yields a deterministic, numerically stable `pcov` scaling, ensuring consistent CI grading across all valid solutions.

## Pinned Uncertainty Propagation (MC) Details
- **Sample Size:** 500 draws.
- **Percentile Interpolation:** `np.percentile` with default linear interpolation.
- **Per-Draw Normalization:** Sign-normalization is applied individually to each of the 500 random samples.
- **RNG Seed:** `1234` and `method='cholesky'`.

## Pinned FFT Seeding Recipe
To ensure two experts reach the same global minimum for the 8-parameter non-linear fit, use the following exact seeding recipe: 
1. After fitting the single-mode model, take the FFT of the residuals. 
2. Take the **two largest FFT peak frequencies** as `omega1` and `omega2` seeds.
3. Use their peak magnitudes as initial guesses for `A1` and `A2`.

## Pinned Scientific Stack
The following library versions are strictly required to ensure numerical reproducibility of `pcov` across platforms:
- `numpy==1.26.0`
- `scipy==1.13.0`
- `lightgbm==4.3.0`

## Note on Grading
The grader ONLY inspects the final values inside `fault_report.json` (imputation accuracy, point estimate, CI bounds, MC standard deviation, and sign-normalization). The exact fitting call, MC sampling code, or choice of optimizer are NOT inspected procedurally. These pinned conventions are strictly disclosed for anti-divergence and reproducibility.