# fetch_wallet_data.py
import requests
import pandas as pd
import streamlit as st

# ✅ Check if the address is a contract using Etherscan
def is_contract(address):
    etherscan_key = st.secrets["api"]["etherscan_v2"]
    url = "https://api.etherscan.io/api"
    params = {
        "module": "contract",
        "action": "getsourcecode",
        "address": address,
        "apikey": etherscan_key
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        result = data.get("result", [{}])[0]
        return result.get("ABI") != "Contract source code not verified"
    except Exception:
        return False

# ✅ Fetch wallet data and features
def fetch_wallet_data(address):
    etherscan_key = st.secrets["api"]["etherscan_v2"]
    covalent_key = st.secrets["api"]["covalent"]
    moralis_key = st.secrets["api"]["moralis"]

    # ------------------------------
    # 1️⃣ Etherscan
    # ------------------------------
    base_url = "https://api.etherscan.io/api"
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": etherscan_key
    }

    try:
        r = requests.get(base_url, params=params, timeout=10)
        data = r.json()
        txs = data.get("result", [])
        print("📦 Etherscan tx count:", len(txs))
    except Exception as e:
        print("❌ Etherscan error:", e)
        txs = []

    # ------------------------------
    # 2️⃣ Covalent Fallback
    # ------------------------------
    if not isinstance(txs, list) or len(txs) == 0:
        url = f"https://api.covalenthq.com/v1/1/address/{address}/transactions_v2/"
        try:
            r = requests.get(url, params={"key": covalent_key}, timeout=10)
            data = r.json()
            items = data.get("data", {}).get("items", [])
            print("📦 Covalent tx count:", len(items))
        except Exception as e:
            print("❌ Covalent error:", e)
            items = []

        if isinstance(items, list) and len(items) > 0:
            df = pd.json_normalize(items)
            df["timestamp"] = pd.to_datetime(df["block_signed_at"], errors="coerce")
            df["value"] = df["value"].astype(float)
            df["to"] = df["to_address"]
            df["gasUsed"] = df.get("gas_spent", 0).astype(float)
        else:
            # ------------------------------
            # 3️⃣ Moralis Fallback
            # ------------------------------
            url = f"https://deep-index.moralis.io/api/v2.2/{address}/transactions?chain=eth"
            headers = {"X-API-Key": moralis_key}
            try:
                r = requests.get(url, headers=headers, timeout=10)
                data = r.json()
                result = data.get("result", [])
                print("📦 Moralis tx count:", len(result))
            except Exception as e:
                print("❌ Moralis error:", e)
                result = []

            if not isinstance(result, list) or len(result) == 0:
                return {
                    "success": True,
                    "data": pd.DataFrame(),
                    "features": {
                        "wallet_age_days": 0,
                        "tx_count": 0,
                        "small_transfer_count": 0,
                        "avg_tx_value": 0,
                        "avg_gas_used": 0,
                        "unique_receivers": 0,
                        "contract_interaction_count": 0,
                        "is_sybil_no_transactions": True,
                        "is_contract": is_contract(address)
                    }
                }

            df = pd.json_normalize(result)
            df["timestamp"] = pd.to_datetime(df["block_timestamp"], errors="coerce")
            df["value"] = df["value"].astype(float)
            df["to"] = df["to_address"]
            df["gasUsed"] = df.get("receipt_gas_used", 0).astype(float)
    else:
        df = pd.DataFrame(txs)
        df["timestamp"] = pd.to_datetime(df["timeStamp"].astype(int), unit="s", errors="coerce")
        df["value"] = df["value"].astype(float)
        df["gasUsed"] = df.get("gasUsed", 0).astype(float)

    # ------------------------------
    # ✅ Final Cleanup & Feature Calculation
    # ------------------------------
    df = df[df["timestamp"].notnull()]
    if df.empty:
        print("⚠️ All timestamps null or invalid — treating as Sybil")
        return {
            "success": True,
            "data": pd.DataFrame(),
            "features": {
                "wallet_age_days": 0,
                "tx_count": 0,
                "small_transfer_count": 0,
                "avg_tx_value": 0,
                "avg_gas_used": 0,
                "unique_receivers": 0,
                "contract_interaction_count": 0,
                "is_sybil_no_transactions": True,
                "is_contract": is_contract(address)
            }
        }

    wallet_age_days = (pd.Timestamp.utcnow() - df["timestamp"].min()).days
    avg_tx_value = df["value"].mean()
    unique_receivers = df["to"].nunique()
    small_tx_count = (df["value"] < 0.01 * 1e18).sum()
    avg_gas_used = df["gasUsed"].mean()
    tx_count = len(df)

    # Count contract interactions
    if "functionName" in df.columns:
        contract_calls = df["functionName"].notnull().sum()
    elif "input" in df.columns:
        contract_calls = (df["input"] != "0x").sum()
    else:
        contract_calls = 0

    return {
        "success": True,
        "data": df,
        "features": {
            "wallet_age_days": wallet_age_days,
            "tx_count": tx_count,
            "small_transfer_count": small_tx_count,
            "avg_tx_value": avg_tx_value,
            "avg_gas_used": avg_gas_used,
            "unique_receivers": unique_receivers,
            "contract_interaction_count": contract_calls,
            "is_sybil_no_transactions": False,
            "is_contract": is_contract(address)
        }
    }
