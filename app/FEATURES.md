# Feature Vector Construction
To run inference on fault_detector.pkl, you must construct a 5-feature vector:
1. max_value (float): Maximum amplitude of the reconstructed signal.
2. min_value (float): Minimum amplitude of the reconstructed signal.
3. std_dev (float): Standard deviation of the reconstructed signal.
4. mean_value (float): Mean of the reconstructed signal.
5. zero_crossing_rate (float): Number of zero crossings divided by total length.