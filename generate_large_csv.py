# generate_large_csv.py
import pandas as pd
import numpy as np

np.random.seed(42)
num_wallets = 10_000

def generate_wallet_data():
    data = []
    for i in range(num_wallets):
        wallet = f"0x{i:040x}"
        tx_count = np.random.randint(1, 5000)
        small_transfers = np.random.randint(0, tx_count)
        avg_gas_used = np.random.normal(loc=40000, scale=10000)
        avg_tx_value = np.random.exponential(scale=0.02)
        wallet_age_days = np.random.randint(30, 3500)
        contract_calls = np.random.randint(0, tx_count)
        sybil_flag = 1 if (small_transfers > tx_count * 0.7 and avg_tx_value < 0.01) else 0
        if np.random.rand() < 0.2:
            sybil_flag = 1 - sybil_flag
        features = {
            "wallet": wallet,
            "tx_count": tx_count,
            "small_transfer_count": small_transfers,
            "avg_gas_used": max(avg_gas_used, 0),
            "avg_tx_value": avg_tx_value,
            "wallet_age_days": wallet_age_days,
            "contract_interaction_count": contract_calls,
            "is_sybil": sybil_flag
        }
        data.append(features)

    df = pd.DataFrame(data)
    df.to_csv("wallet_data_large.csv", index=False)
    print("✅ wallet_data_large.csv generated successfully.")

# Run
if __name__ == "__main__":
    generate_wallet_data()
