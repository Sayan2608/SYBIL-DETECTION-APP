# train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load the data
df = pd.read_csv("wallet_data_large.csv")

X = df[[
    "wallet_age_days",
    "tx_count",
    "small_transfer_count",
    "avg_tx_value",
    "avg_gas_used",
    "contract_interaction_count"
]]
y = df["is_sybil"]

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Predict on training data
y_pred = model.predict(X)

# Accuracy metrics
acc = accuracy_score(y, y_pred)
print(f"✅ Training Accuracy: {acc*100:.2f}%\n")

print("✅ Classification Report:")
print(classification_report(y, y_pred))

# Feature importances
importances = model.feature_importances_
feature_names = X.columns

print("\n✅ Feature Importances:")
for name, score in zip(feature_names, importances):
    print(f"{name}: {score:.3f}")

# Save the model
joblib.dump(model, "sybil_model.pkl")
print("\n✅ Model trained and saved successfully.")