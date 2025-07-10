import pandas as pd
import requests
from datetime import datetime
import json
import streamlit as st

def fetch_wallet_data(chain, wallet_address):
    if chain in ["Ethereum", "BNB", "Polygon", "Arbitrum", "Optimism"]:
        # Map chain to correct API
        api_map = {
            "Ethereum": "etherscan",
            "BNB": "bscscan",
            "Polygon": "polygonscan",
            "Arbitrum": "arbiscan",
            "Optimism": "optimism"
        }
        api_key = st.secrets["api"][api_map[chain]]

        base_url = {
            "Ethereum": "https://api.etherscan.io",
            "BNB": "https://api.bscscan.com",
            "Polygon": "https://api.polygonscan.com",
            "Arbitrum": "https://api.arbiscan.io",
            "Optimism": "https://api-optimistic.etherscan.io"
        }[chain]

        tx_url = (
            f"{base_url}/api"
            f"?module=account&action=txlist"
            f"&address={wallet_address}"
            f"&startblock=0&endblock=99999999&sort=asc"
            f"&apikey={api_key}"
        )

        response = requests.get(tx_url)

        if response.status_code != 200:
            return {"success": False, "error": f"API error: {response.status_code}"}

        res_json = response.json()
        if res_json["status"] != "1":
            return {"success": False, "error": res_json.get("message", "Unknown error")}

        txs = pd.DataFrame(res_json["result"])

        if txs.empty:
            return {"success": True, "data": txs, "features": {}}

        txs["value"] = txs["value"].astype(float) / 1e18
        txs["gasUsed"] = txs["gasUsed"].astype(float)
        txs["timeStamp"] = pd.to_datetime(txs["timeStamp"], unit="s")

        wallet_age_days = (pd.Timestamp.now() - txs["timeStamp"].min()).days
        avg_tx_value = txs["value"].mean()
        unique_receivers = txs["to"].nunique()
        small_tx_count = (txs["value"] < 0.01).sum()
        avg_gas_used = txs["gasUsed"].mean()

        features = {
            "wallet_age_days": wallet_age_days,
            "avg_tx_value": avg_tx_value,
            "unique_receivers": unique_receivers,
            "small_tx_count": small_tx_count,
            "avg_gas_used": avg_gas_used
        }

        return {"success": True, "data": txs, "features": features}

    elif chain in ["Solana", "Sui", "Near"]:
        # Placeholder for other chains
        return {"success": False, "error": f"{chain} support not implemented yet."}

    else:
        return {"success": False, "error": "Unsupported chain"}
