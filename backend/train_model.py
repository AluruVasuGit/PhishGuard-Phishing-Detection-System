import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_csv("dataset/5.urldata.csv")

# Drop 'Domain' as it is not a numerical feature
df.drop(columns=['Domain'], inplace=True)

# Split features and target variable
X = df.drop(columns=['Label'])
y = df['Label']

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model
model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
model.fit(X_train_scaled, y_train)

# Save the trained model and scaler
model_data = {
    "model": model,
    "scaler": scaler,
    "features": list(X.columns)
}

with open("phishing_model.pkl", "wb") as file:
    pickle.dump(model_data, file)

print("Model training complete. Model saved as phishing_model.pkl")
