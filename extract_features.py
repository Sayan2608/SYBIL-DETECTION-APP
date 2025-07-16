# extract_features.py
import pandas as pd
from fetch_wallet_data import fetch_wallet_data

# Replace these with real Ethereum wallet addresses
wallets = [
    "0x000000000000000000000000000000000000dead",
    "0xF977814e90dA44bFA03b6295A0616a897441aceC",
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
    "0xFE9e8709d3215310075d67E3ed32A380CCf451C8",
    # Add more wallet addresses here
]

results = []

for wallet in wallets:
    print(f"Fetching {wallet}...")
    result = fetch_wallet_data(wallet)

    if result["success"]:
        features = result["features"]
        features["wallet"] = wallet
        features["is_sybil"] = None  # You will fill 0 or 1 manually later
        results.append(features)
    else:
        print(f"Failed to fetch: {wallet} | {result.get('error')}")

df = pd.DataFrame(results)
df.to_csv("real_wallet_data.csv", index=False)
print("✅ Saved to real_wallet_data.csv")
