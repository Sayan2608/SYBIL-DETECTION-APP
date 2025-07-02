import streamlit as st
import pandas as pd
import requests
import joblib
import os
from datetime import datetime

# Load Etherscan API key from secrets
ETHERSCAN_API_KEY = st.secrets["api"]["etherscan"]

# Load ML model
model = joblib.load("sybil_model.pkl")

st.set_page_config(page_title="Sybil Wallet Checker", layout="wide")
st.title("🧠 Ethereum Sybil Wallet Checker")

wallet_address = st.text_input("🔗 Enter Ethereum Wallet Address")

if st.button("Check Wallet") and wallet_address:
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={wallet_address}&startblock=0&endblock=99999999&sort=asc&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data["status"] == "1" and data["result"]:
            txs = pd.DataFrame(data["result"])
            
            # Clean and convert
            txs["value"] = txs["value"].astype(float) / 1e18
            txs["gasUsed"] = txs["gasUsed"].astype(float)
            txs["timeStamp"] = pd.to_datetime(txs["timeStamp"], unit="s")
            
            # Feature engineering
            wallet_age_days = (pd.Timestamp.now() - txs["timeStamp"].min()).days
            unique_receivers = txs["to"].nunique()
            avg_tx_value = txs["value"].mean()
            small_tx_count = (txs["value"] < 0.01).sum()
            avg_gas_used = txs["gasUsed"].mean()

            # Display summary metrics
            st.subheader("📊 Wallet Metrics")
            col1, col2, col3 = st.columns(3)
            col1.metric("📅 Wallet Age", f"{wallet_age_days} days")
            col2.metric("💸 Avg Tx Value", f"{avg_tx_value:.5f} ETH")
            col3.metric("⛽ Avg Gas Used", f"{avg_gas_used:,.0f}")
            
            col4, col5 = st.columns(2)
            col4.metric("📉 Small Transfers (<0.01 ETH)", small_tx_count)
            col5.metric("👥 Unique Receivers", unique_receivers)

            # Prepare features for prediction
            features = pd.DataFrame([{
                "wallet_age_days": wallet_age_days,
                "unique_receivers": unique_receivers,
                "avg_tx_value": avg_tx_value,
                "small_tx_count": small_tx_count,
                "avg_gas_used": avg_gas_used
            }])
            prediction = model.predict(features)[0]

            # Show result
            st.subheader("🔎 Sybil Risk Analysis")
            if prediction == 1:
                st.error("🔴 High Sybil Risk – Suspicious activity detected.")
            else:
                st.success("🟢 Low Sybil Risk – Wallet appears normal.")

            # Charts
            st.subheader("📈 Transaction Value Over Time")
            st.line_chart(txs.set_index("timeStamp")["value"])

            st.subheader("⛽ Gas Used Over Time")
            st.bar_chart(txs.set_index("timeStamp")["gasUsed"])

            # Show recent transactions
            st.subheader("📋 Recent Transactions")
            st.dataframe(txs[["hash", "from", "to", "value", "gasUsed", "timeStamp"]].tail(10))

        else:
            st.warning("⚠️ No transactions found or invalid wallet.")
    else:
        st.error("❌ Failed to fetch data from Etherscan.")