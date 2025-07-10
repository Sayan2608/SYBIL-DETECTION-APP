# chain_api.py
import requests
import os
import pandas as pd

def fetch_solana_transactions(wallet):
    api_key = os.getenv("HELIUS_API_KEY")
    url = f"https://rpc.helius.xyz/?api-key={api_key}"
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",
        "params": [wallet, {"limit": 100}]
    }
    r = requests.post(url, json=payload)
    txs = []
    if r.ok:
        for t in r.json().get("result", []):
            txs.append({
                "hash": t["signature"],
                "timeStamp": pd.to_datetime(t["blockTime"], unit="s") if t.get("blockTime") else pd.Timestamp.now(),
                "value": 0,
                "gasUsed": 0,
                "to": "",
                "from": ""
            })
    return txs

def fetch_sui_transactions(wallet):
    url = "https://fullnode.mainnet.sui.io:443"
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "sui_getTransactions",
        "params": [{"ToAddress": wallet}, "desc", 100, None]
    }
    r = requests.post(url, json=payload)
    txs = []
    if r.ok:
        for t in r.json().get("result", []):
            txs.append({
                "hash": t,
                "timeStamp": pd.Timestamp.now(),
                "value": 0,
                "gasUsed": 0,
                "to": "",
                "from": ""
            })
    return txs

def fetch_near_transactions(wallet):
    # Near needs an indexer for real data, this is placeholder
    return []
