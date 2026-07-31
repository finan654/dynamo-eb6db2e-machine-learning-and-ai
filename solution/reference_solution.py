import numpy as np
import pandas as pd
import pickle
from scipy.optimize import curve_fit
from scipy.fft import rfft, rfftfreq
import json
import os

# 1. Pinned RNG
rng = np.random.default_rng(1234)

# 2. Load Data
df = pd.read_csv('app/data/sensor_telemetry.csv')
t_full = df['t'].values
x_full = df['x'].values
missing_mask = np.isnan(x_full)
observed_mask = ~missing_mask

t_obs = t_full[observed_mask]
x_obs = x_full[observed_mask]

# 3. Single Mode Fit (FFT seed guess)
t_even = np.linspace(t_obs[0], t_obs[-1], len(t_obs))
x_even = np.interp(t_even, t_obs, x_obs) # simple interpolation for FFT
fft_vals = np.abs(rfft(x_even - np.mean(x_even)))
freqs = rfftfreq(len(x_even), d=(t_even[1]-t_even[0]))
omega_guess = 2 * np.pi * freqs[np.argmax(fft_vals[1:]) + 1]

def model1(t, A, g, w, p):
    return A * np.exp(-g * t) * np.cos(w * t + p)

# CRITICAL: NO sigma, NO absolute_sigma. Defaults only.
popt1, _ = curve_fit(model1, t_obs, x_obs, p0=[1.0, 0.5, omega_guess, 0.0])

# 4. Detect residual via FFT
residuals = x_obs - model1(t_obs, *popt1)
fft_res = np.abs(rfft(residuals - np.mean(residuals)))
freqs_res = rfftfreq(len(residuals), d=(t_obs[1]-t_obs[0]))
peak_freq = freqs_res[np.argmax(fft_res[1:]) + 1]
omega2_guess = 2 * np.pi * peak_freq

# 5. Two Mode Joint Fit
def model2(t, A1, g1, w1, p1, A2, g2, w2, p2):
    return (A1 * np.exp(-g1 * t) * np.cos(w1 * t + p1) +
            A2 * np.exp(-g2 * t) * np.cos(w2 * t + p2))

# CRITICAL: NO sigma, NO absolute_sigma. Defaults only.
popt2, pcov = curve_fit(model2, t_obs, x_obs, 
                        p0=[popt1[0], popt1[1], popt1[2], popt1[3], 1.0, 0.3, omega2_guess, 0.0])

# 6. Normalize signs (A >= 0, phi in [0, 2pi))
# Note: pcov corresponds to the raw popt2 before normalization. 
# Normalization ensures A >=0 and phi in [0,2pi), but leaves the model's final curve invariant.
for i in range(0, 8, 4):
    if popt2[i] < 0:
        popt2[i] *= -1
        popt2[i+3] += np.pi
    popt2[i+3] = popt2[i+3] % (2 * np.pi)

# 7. Reconstruct only missing block
x_imputed = x_full.copy()
x_imputed[missing_mask] = model2(t_full[missing_mask], *popt2)

# 8. Build Features
features = np.array([
    np.max(x_imputed), np.min(x_imputed), np.std(x_imputed),
    np.mean(x_imputed), np.sum(np.diff(np.sign(x_imputed)) != 0) / len(x_imputed)
]).reshape(1, -1)

# 9. Load Model & Predict
with open('app/models/fault_detector.pkl', 'rb') as f:
    clf = pickle.load(f)
p_fault = clf.predict_proba(features)[0, 1]

# 10. Uncertainty Propagation (Pinned RNG & Pinned Matrix Decomposition)
# Added method='cholesky' to fix sign-flip ambiguities in SVD across near-identical pcovs.
samples = rng.multivariate_normal(popt2, pcov, size=500, method='cholesky')
probs = []
for params in samples:
    x_sample = x_full.copy()
    x_sample[missing_mask] = model2(t_full[missing_mask], *params)
    feat_sample = np.array([np.max(x_sample), np.min(x_sample), np.std(x_sample),
                            np.mean(x_sample), np.sum(np.diff(np.sign(x_sample)) != 0) / len(x_sample)]).reshape(1, -1)
    probs.append(clf.predict_proba(feat_sample)[0, 1])

ci_lower, ci_upper = np.percentile(probs, [2.5, 97.5])
fault_detected = bool(p_fault > 0.5 and ci_lower <= p_fault <= ci_upper)

# 11. Save Output
output = {
    'fault_detected': fault_detected,
    'p_fault': float(p_fault),
    'confidence_lower': float(ci_lower),
    'confidence_upper': float(ci_upper)
}
os.makedirs('app/outputs', exist_ok=True)
with open('app/outputs/fault_report.json', 'w') as f:
    json.dump(output, f, indent=4)

print("Reference solution executed successfully. Output saved to app/outputs/fault_report.json")