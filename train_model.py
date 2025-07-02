# train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Load generated data
df = pd.read_csv("wallet_data.csv")

# Features and labels
features = [ 
    "tx_count",
    "small_transfer_count",
    "avg_gas_used",
    "avg_tx_value",
    "wallet_age_days",
    "contract_interaction_count"
]
X = df[features]
y = df["is_sybil"]

# Train/test model
X_train , X_test , y_train , y_test =  train_test_split(X,y, test_size=0.2, random_state=42)

#train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save with joblib (preserves feature names)
joblib.dump(model, "sybil_model.pkl")
print("✅ Model trained and saved as sybil_model.pkl")
