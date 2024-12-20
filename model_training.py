import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Example: Simple dummy model
X = np.array([[10, 5], [20, 10], [30, 15], [40, 20], [50, 25]])  # Example features
y = [0, 1, 0, 1, 0]  # Example labels: 0 = Healthy, 1 = At Risk

model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Save the trained model
joblib.dump(model, "model.pkl")
print("Model saved as 'model.pkl'")
