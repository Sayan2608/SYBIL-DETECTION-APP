import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load your training data
df = pd.read_csv("wallet_data.csv")

# Show the columns to confirm
print("Columns in CSV:", df.columns.tolist())

# Features and labels (matching your actual CSV)
X = df[[
    "wallet_age_days",
    "unique_receivers",
    "small_tx_count",
    "avg_tx_value",
    "avg_gas_used"
]]
y = df["label"]

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save the model
joblib.dump(model, "sybil_model.pkl")

print("✅ Model trained and saved successfully.")
