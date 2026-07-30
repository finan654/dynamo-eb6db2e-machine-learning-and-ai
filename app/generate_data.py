import numpy as np
import pandas as pd
import os

# Set seed
rng = np.random.default_rng(42)

# Define the 2-mode damped oscillator
t = np.linspace(0, 10, 1000)
A1, g1, w1, p1 = 2.0, 0.5, 5.0, 0.0
A2, g2, w2, p2 = 1.5, 0.3, 5.8, 0.5  # w2 is 16% larger than w1, within the 12-18% trap range
sigma_noise = 0.1

x = A1 * np.exp(-g1 * t) * np.cos(w1 * t + p1) + A2 * np.exp(-g2 * t) * np.cos(w2 * t + p2)
x += rng.normal(0, sigma_noise, len(t))

# Add 30% missing block in the middle
start_missing, end_missing = 350, 650
x[start_missing:end_missing] = np.nan

# Save to the app/data folder
df = pd.DataFrame({'t': t, 'x': x})
os.makedirs('app/data', exist_ok=True)
df.to_csv('app/data/sensor_telemetry.csv', index=False)
print("Data generated successfully at app/data/sensor_telemetry.csv")
