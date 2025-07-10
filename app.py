import streamlit as st
import pandas as pd
import requests
import joblib
from datetime import datetime
import os

# Load ML model
model = joblib.load("sybil_model.pkl")

# Streamlit config
st.set_page_config(page_title="Sybil Wallet Checker", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 6px;
        padding: 0.5em 1em;
        font-weight: bold;
        font-size: 1em;
    }
    .footer {
        text-align: center;
        color: #888;
        margin-top: 40px;
        font-size: 0.9em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Admin unlock
ADMIN_UNLOCK_CODE = "260804"
st.sidebar.title("Admin")
admin_code = st.sidebar.text_input("Enter admin unlock code", type="password")
is_admin = admin_code == ADMIN_UNLOCK_CODE

# Title
st.title("🧠 Multichain Sybil Wallet Checker")
st.write("Select a blockchain and enter a wallet address to get free Sybil risk screening.")

# Select blockchain
chain = st.selectbox(
    "Select Blockchain",
    [
        "Ethereum",
        "BNB Chain",
        "Polygon",
        "Arbitrum",
        "Optimism",
        "Solana",
        "Sui",
        "Near"
    ]
)

# Input wallet address
wallet_address = st.text_input("🔗 Wallet Address")

# Button
if st.button("🔍 Analyze Wallet") and wallet_address:
    st.info(f"🔗 Analyzing {wallet_address} on {chain}...")

    txs = None
    eth_balance = None

    if chain in ["Ethereum", "BNB Chain", "Polygon", "Arbitrum", "Optimism"]:
        # Map API URLs
        api_map = {
            "Ethereum": "https://api.etherscan.io/api",
            "BNB Chain": "https://api.bscscan.com/api",
            "Polygon": "https://api.polygonscan.com/api",
            "Arbitrum": "https://api.arbiscan.io/api",
            "Optimism": "https://api-optimistic.etherscan.io/api"
        }
        api_key_env = {
            "Ethereum": "ETHERSCAN_API_KEY",
            "BNB Chain": "BSCSCAN_API_KEY",
            "Polygon": "POLYGONSCAN_API_KEY",
            "Arbitrum": "ARBISCAN_API_KEY",
            "Optimism": "OPTISCAN_API_KEY"
        }

        api_url = api_map[chain]
        api_key = os.getenv(api_key_env[chain])

        tx_url = (
            f"{api_url}?module=account&action=txlist"
            f"&address={wallet_address}"
            f"&startblock=0&endblock=99999999&sort=asc"
            f"&apikey={api_key}"
        )
        balance_url = (
            f"{api_url}?module=account&action=balance"
            f"&address={wallet_address}"
            f"&tag=latest"
            f"&apikey={api_key}"
        )

        tx_response = requests.get(tx_url)
        balance_response = requests.get(balance_url)

        if tx_response.status_code == 200 and tx_response.json()["status"] == "1":
            txs = pd.DataFrame(tx_response.json()["result"])
            txs["value"] = txs["value"].astype(float) / 1e18
            txs["gasUsed"] = txs["gasUsed"].astype(float)
            txs["timeStamp"] = pd.to_datetime(txs["timeStamp"], unit="s")
            eth_balance = float(balance_response.json()["result"]) / 1e18 if balance_response.ok and balance_response.json().get("status") == "1" else None
        else:
            st.error("❌ Could not fetch transactions. Try a different address or check the API key.")
            st.stop()

    elif chain in ["Solana", "Sui", "Near"]:
        st.warning(f"⚠️ {chain} support not yet implemented. Please integrate RPC logic here.")
        st.stop()

    else:
        st.error("❌ Unsupported blockchain selected.")
        st.stop()

    # Feature engineering
    wallet_age_days = (pd.Timestamp.now() - txs["timeStamp"].min()).days
    avg_tx_value = txs["value"].mean()
    unique_receivers = txs["to"].nunique()
    small_tx_count = (txs["value"] < 0.01).sum()
    avg_gas_used = txs["gasUsed"].mean()

    features = pd.DataFrame([{
        "wallet_age_days": wallet_age_days,
        "unique_receivers": unique_receivers,
        "small_tx_count": small_tx_count,
        "avg_tx_value": avg_tx_value,
        "avg_gas_used": avg_gas_used
    }])

    prediction = model.predict(features)[0]

    # Display results
    st.subheader(f"✅ Basic Free Results ({chain})")
    st.metric("Wallet Age", f"{wallet_age_days} days")
    st.metric("Average Tx Value", f"{avg_tx_value:.5f}")

    if prediction == 1:
        st.error("🔴 High Sybil Risk detected.")
    else:
        st.success("🟢 Low Sybil Risk detected.")

    # Admin section
    if is_admin:
        st.markdown("---")
        st.subheader("🔐 Full Wallet Analysis")

        st.metric("Unique Receivers", unique_receivers)
        st.metric("Small Transfers", small_tx_count)
        st.metric("Avg Gas Used", f"{avg_gas_used:,.0f}")

        st.write("📈 Transaction Value Over Time")
        st.line_chart(txs.set_index("timeStamp")["value"])

        st.write("⛽ Gas Used Over Time")
        st.bar_chart(txs.set_index("timeStamp")["gasUsed"])

        st.write("📋 Recent Transactions")
        st.dataframe(txs[["hash", "from", "to", "value", "gasUsed", "timeStamp"]].tail(10))

        if eth_balance is not None:
            st.metric("💰 Balance", f"{eth_balance:.4f} ETH")
    else:
        st.markdown("---")
        st.subheader("🔒 Full Analysis Unlock")
        st.markdown("""
        **Upgrade to get:**
        - Full transaction analytics
        - Gas usage charts
        - Recent transaction logs
        - Balance tracking
        """)

# Footer
st.markdown(
    """
    <div class="footer">
        © 2025 Sybil Wallet Checker • Built with ❤️ by Sayan Rawl <br>
        <a href="mailto:sayanrawl7@email.com" target="_blank">Contact</a> |
        <a href="https://twitter.com/RawlSayan58006" target="_blank">Twitter</a>
    </div>
    """,
    unsafe_allow_html=True
)
