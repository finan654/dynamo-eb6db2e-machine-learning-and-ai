## Pinned FFT Seeding & Ordering Rules
- To ensure all solvers reach the same global minimum, seed the fit using the **two largest peaks of the residual FFT**. Largest peak = omega1 seed, second largest = omega2 seed. Peak magnitudes = A seeds. Set gamma = 0.5 and phi = 0.0 for initial guesses.
- **Ordering rule:** If ambiguity arises between two modes, order them strictly by **descending frequency** (omega1 > omega2) to prevent order-dependent pcov shifts.
- **pcov normalization:** The `pcov` uses the standard residual-variance normalization from `curve_fit`'s default no-sigma convention.