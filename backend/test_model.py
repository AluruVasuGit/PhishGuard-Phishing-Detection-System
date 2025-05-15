import pickle
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
df = pd.read_csv("dataset/5.urldata.csv")
df.drop(columns=['Domain'], inplace=True)

# Split features and target variable
X = df.drop(columns=['Label'])
y = df['Label']

# Load trained model
with open("phishing_model.pkl", "rb") as file:
    model_data = pickle.load(file)

model = model_data["model"]
scaler = model_data["scaler"]

# Transform data
X_scaled = scaler.transform(X)

# Predict
y_pred = model.predict(X_scaled)

# Evaluate
accuracy = accuracy_score(y, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")
print("\nClassification Report:\n", classification_report(y, y_pred))
