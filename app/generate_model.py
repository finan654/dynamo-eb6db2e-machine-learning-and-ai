import numpy as np
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier

# Generate random fake data for the LightGBM (we'll use RandomForest as a proxy) 
# to ensure the file exists
rng = np.random.default_rng(1234)
X_train = rng.normal(0, 1, (1000, 5))
y_train = rng.integers(0, 2, 1000)

# Train a simple classifier
clf = RandomForestClassifier(n_estimators=10, random_state=42)
clf.fit(X_train, y_train)

# Save it to the app/models folder
with open('app/models/fault_detector.pkl', 'wb') as f:
    pickle.dump(clf, f)

print("Mock fault_detector.pkl created successfully in app/models/")