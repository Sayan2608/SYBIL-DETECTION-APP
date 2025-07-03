import streamlit as st
import pandas as pd
import requests
import joblib
from datetime import datetime
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Sybil Wallet Checker", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    h1 {
        color: #4CAF50;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-weight: bold;
    }
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        text-align: center;
        font-size: 0.9em;
        color: gray;
        padding: 10px;
        background-color: rgba(255,255,255,0.9);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🧠 Ethereum Sybil Wallet Checker")

wallet_address = st.text_input("🔗 Enter Ethereum Wallet Address")

# Load model
model = joblib.load("sybil_model.pkl")

if st.button("Check Wallet") and wallet_address:
    # Fetch transaction history
    tx_url = (
        f"https://api.etherscan.io/api"
        f"?module=account&action=txlist"
        f"&address={wallet_address}"
        f"&startblock=0&endblock=99999999&sort=asc"
        f"&apikey={st.secrets['api']['etherscan']}"
    )
    tx_response = requests.get(tx_url)

    # Fetch ETH balance
    balance_url = (
        f"https://api.etherscan.io/api"
        f"?module=account&action=balance"
        f"&address={wallet_address}"
        f"&tag=latest"
        f"&apikey={st.secrets['api']['etherscan']}"
    )
    balance_response = requests.get(balance_url)

    if tx_response.status_code == 200:
        tx_data = tx_response.json()
        if tx_data["status"] == "1" and tx_data["result"]:
            txs = pd.DataFrame(tx_data["result"])
            txs["value"] = txs["value"].astype(float) / 1e18
            txs["gasUsed"] = txs["gasUsed"].astype(float)
            txs["timeStamp"] = pd.to_datetime(txs["timeStamp"], unit="s")

            # Feature engineering
            wallet_age_days = (pd.Timestamp.now() - txs["timeStamp"].min()).days
            unique_receivers = txs["to"].nunique()
            avg_tx_value = txs["value"].mean()
            small_tx_count = (txs["value"] < 0.01).sum()
            avg_gas_used = txs["gasUsed"].mean()
            total_gas = txs["gasUsed"].sum()

            # Prediction
            features = pd.DataFrame([{
                "wallet_age_days": wallet_age_days,
                "unique_receivers": unique_receivers,
                "avg_tx_value": avg_tx_value,
                "small_tx_count": small_tx_count,
                "avg_gas_used": avg_gas_used
            }])
            prediction = model.predict(features)[0]

            # Tabs
            tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
                "📊 Wallet Metrics",
                "🔎 Sybil Risk Analysis",
                "📈 Transaction Value",
                "⛽ Gas Used",
                "🍰 Size Distribution",
                "📊 Gas Histogram",
                "📋 Recent Transactions",
                "💰 ETH Balance"
            ])

            with tab1:
                st.subheader("📊 Wallet Metrics")
                col1, col2, col3 = st.columns(3)
                col1.metric("📅 Wallet Age", f"{wallet_age_days} days")
                col2.metric("💸 Avg Tx Value", f"{avg_tx_value:.5f} ETH")
                col3.metric("⛽ Avg Gas Used", f"{avg_gas_used:,.0f}")
                col1.metric("⛽ Total Gas Used", f"{total_gas:,.0f}")
                col2.metric("📉 Small Transfers", small_tx_count)
                col3.metric("👥 Unique Receivers", unique_receivers)

            with tab2:
                st.subheader("🔎 Sybil Risk Analysis")
                if prediction == 1:
                    st.error("🔴 High Sybil Risk – Suspicious activity detected.")
                else:
                    st.success("🟢 Low Sybil Risk – Wallet appears normal.")

            with tab3:
                st.subheader("📈 Transaction Value Over Time")
                st.line_chart(txs.set_index("timeStamp")["value"])

            with tab4:
                st.subheader("⛽ Gas Used Over Time")
                st.bar_chart(txs.set_index("timeStamp")["gasUsed"])

            with tab5:
                st.subheader("🍰 Transaction Size Distribution")
                small = (txs["value"] < 0.01).sum()
                large = (txs["value"] >= 0.01).sum()
                fig1, ax1 = plt.subplots()
                ax1.pie(
                    [small, large],
                    labels=["Small (<0.01 ETH)", "Large"],
                    autopct="%1.1f%%",
                    colors=["#4CAF50", "#2196F3"]
                )
                st.pyplot(fig1)

            with tab6:
                st.subheader("📊 Gas Usage Histogram")
                fig2, ax2 = plt.subplots()
                ax2.hist(txs["gasUsed"], bins=20, color="#4CAF50")
                ax2.set_xlabel("Gas Used")
                ax2.set_ylabel("Count")
                st.pyplot(fig2)

            with tab7:
                st.subheader("📋 Recent Transactions")
                st.dataframe(
                    txs[["hash", "from", "to", "value", "gasUsed", "timeStamp"]].tail(10)
                )

            with tab8:
                st.subheader("💰 ETH Balance")
                if balance_response.status_code == 200:
                    balance_data = balance_response.json()
                    if balance_data["status"] == "1":
                        eth_balance = float(balance_data["result"]) / 1e18
                        st.metric("ETH Balance", f"{eth_balance:.4f} ETH")
                    else:
                        st.warning("Could not fetch ETH balance.")
                else:
                    st.error("Error fetching ETH balance.")

        else:
            st.warning("⚠️ No transactions found or invalid wallet.")
    else:
        st.error("❌ Failed to fetch data from Etherscan.")

# Footer
st.markdown(
    """
    <div class="footer">
        © 2025 Sybil Wallet Checker • Built with ❤️ using Streamlit<br>
        <a href="mailto:sayanrawl7@email.com" target="_blank" style="margin-right: 15px; text-decoration: none; color: #4CAF50;">💬 Contact</a>
        |
        <a href="https://twitter.com/RawlSayan58006" target="_blank" style="margin-left: 15px; text-decoration: none; color: #4CAF50;">🐦 Twitter</a>
    </div>
    """,
    unsafe_allow_html=True
)
