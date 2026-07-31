# Task Instructions & Pinned Conventions

## Pinned curve_fit Convention
Justification for `no-sigma`: While `absolute_sigma=True` is physically correct for known measurement error, it scales the covariance matrix (`pcov`) by the reduced chi-square based on the exact fit residuals. This breaks reproducibility across identical solver fits due to floating-point differences. The pinned `no-sigma` convention yields a deterministic, numerically stable `pcov` scaling, ensuring consistent CI grading across all valid solutions.