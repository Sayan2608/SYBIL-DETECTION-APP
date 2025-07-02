from datetime import datetime


from datetime import date, timedelta
import pandas as pd
import random

def generate_wallet_data(num_samples=200):
    data = {
         "wallet_address":  [f"0x{random.randint(10**15, 10**16 -1):x}" for _ in range(num_samples)],
         "wallet_age_days": [random.randint(1, 1000) for _ in range(num_samples)],
         "unique_receivers": [random.randint(1, 100) for _ in range(num_samples)],
         "small_tx_count": [random.randint(1, 50) for _ in range(num_samples)],
         "avg_tx_value": [round(random.uniform(0.0001, 1.0),5) for _ in range(num_samples)],
         "avg_gas_used": [random.randint(0, 1) for _ in range(num_samples)],
         "timestamp": [(date.today()-timedelta(days=random.randint(1,1000))).strftime("%Y-%m-%d") for _ in range(num_samples)],
         "label": [random.choice([0,1]) for _ in range(num_samples)] # 1 = Sybil , 0 = Normal 
    }
    return pd.DataFrame(data)

df = generate_wallet_data()
df.to_csv("wallet_data.csv", index=False)
print("✅ wallet_data.csv created")
