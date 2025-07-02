# generate_csv.py
import pandas as pd
import numpy as np

# Simulate fake wallet transaction data
np.random.seed(42)
num_wallets = 100

def generate_wallet_data():
    data = []
    for i in range(num_wallets):
        wallet = f"0x{i:040x}"
        tx_count = np.random.randint(5, 100)
        small_transfers = np.random.randint(0, tx_count)
        gas_used = np.random.normal(loc=30000, scale=5000, size=tx_count)
        tx_values = np.random.exponential(scale=0.01, size=tx_count)
        timestamps = pd.date_range(end=pd.Timestamp.now(), periods=tx_count).to_pydatetime().tolist()
        contract_calls = np.random.randint(0, tx_count)

        features = {
            "wallet": wallet,
            "tx_count": tx_count,
            "small_transfer_count": small_transfers,
            "avg_gas_used": np.mean(gas_used),
            "avg_tx_value": np.mean(tx_values),
            "wallet_age_days": (pd.Timestamp.now() - timestamps[0]).days,
            "contract_interaction_count": contract_calls,
            "is_sybil": np.random.choice([0, 1], p=[0.7, 0.3])
        }
        data.append(features)

    df = pd.DataFrame(data)
    df.to_csv("wallet_data.csv", index=False)
    print("✅ wallet_data.csv generated")

generate_wallet_data()



