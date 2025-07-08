import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load your training data
df = pd.read_csv("wallet_data.csv")

# Show the columns to confirm
print("Columns in CSV:", df.columns.tolist())

# Features and labels
X = df[[
    "wallet_age_days",
    "unique_receivers",
    "avg_tx_value",
    "small_tx_count",
    "avg_gas_used"
]]
y = df["label"]

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save the model
joblib.dump(model, "sybil_model.pkl")

print("✅ Model trained and saved successfully.")
