import streamlit as st
import pandas as pd
import requests
import joblib
from datetime import datetime
import matplotlib.pyplot as plt
from generate_report import generate_sybil_report

# Set your admin code
ADMIN_UNLOCK_CODE = "260804"

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

# Sidebar admin unlock
st.sidebar.title("Admin")
admin_code = st.sidebar.text_input("Enter admin unlock code", type="password")
is_admin = admin_code == ADMIN_UNLOCK_CODE

# Main title
st.title("🧠 Ethereum Sybil Wallet Checker")
st.write("Enter an Ethereum wallet address to get a free basic Sybil risk screening.")

# Input
wallet_address = st.text_input("🔗 **Ethereum Wallet Address**")

if st.button("🔍 Analyze Wallet") and wallet_address:
    with st.spinner("🔄 Fetching transaction data..."):
        tx_url = (
            f"https://api.etherscan.io/api"
            f"?module=account&action=txlist"
            f"&address={wallet_address}"
            f"&startblock=0&endblock=99999999&sort=asc"
            f"&apikey={st.secrets['api']['etherscan']}"
        )
        balance_url = (
            f"https://api.etherscan.io/api"
            f"?module=account&action=balance"
            f"&address={wallet_address}"
            f"&tag=latest"
            f"&apikey={st.secrets['api']['etherscan']}"
        )

        tx_response = requests.get(tx_url)
        balance_response = requests.get(balance_url)

    if tx_response.status_code == 200 and tx_response.json()["status"] == "1":
        txs = pd.DataFrame(tx_response.json()["result"])
        txs["value"] = txs["value"].astype(float) / 1e18
        txs["gasUsed"] = txs["gasUsed"].astype(float)
        txs["timeStamp"] = pd.to_datetime(txs["timeStamp"], unit="s")

        # Feature engineering
        wallet_age_days = (pd.Timestamp.now() - txs["timeStamp"].min()).days
        avg_tx_value = txs["value"].mean()
        unique_receivers = txs["to"].nunique()
        small_tx_count = (txs["value"] < 0.01).sum()
        avg_gas_used = txs["gasUsed"].mean()

        features = pd.DataFrame([{
            "wallet_age_days": wallet_age_days,
            "unique_receivers": unique_receivers,
            "avg_tx_value": avg_tx_value,
            "small_tx_count": small_tx_count,
            "avg_gas_used": avg_gas_used
        }])

        prediction = model.predict(features)[0]

        st.subheader("✅ Basic Free Results")
        st.metric("Wallet Age", f"{wallet_age_days} days")
        st.metric("Average Tx Value", f"{avg_tx_value:.5f} ETH")
        if prediction == 1:
            st.error("🔴 High Sybil Risk detected.")
        else:
            st.success("🟢 Low Sybil Risk detected.")

        # Admin-only: show full analytics + PDF export
        if is_admin:
            st.markdown("---")
            st.subheader("🔐 Full Wallet Analysis")

            st.metric("Unique Receivers", unique_receivers)
            st.metric("Small Transfers", small_tx_count)
            st.metric("Avg Gas Used", f"{avg_gas_used:,.0f}")

            # Value chart
            st.write("📈 Transaction Value Over Time")
            st.line_chart(txs.set_index("timeStamp")["value"])

            # Gas chart
            st.write("⛽ Gas Used Over Time")
            st.bar_chart(txs.set_index("timeStamp")["gasUsed"])

            # Recent transactions
            st.write("📋 Recent Transactions")
            st.dataframe(txs[["hash", "from", "to", "value", "gasUsed", "timeStamp"]].tail(10))

            # ETH balance
            if balance_response.status_code == 200 and balance_response.json()["status"] == "1":
                eth_balance = float(balance_response.json()["result"]) / 1e18
                st.metric("💰 ETH Balance", f"{eth_balance:.4f} ETH")

            # Generate and download PDF
            pdf_bytes = generate_sybil_report(
                wallet_address,
                {
                    "Wallet Age": f"{wallet_age_days} days",
                    "Avg Tx Value": f"{avg_tx_value:.5f} ETH",
                    "Unique Receivers": unique_receivers,
                    "Small Transfers": small_tx_count,
                    "Avg Gas Used": f"{avg_gas_used:,.0f}"
                },
                txs,
                prediction
            )
            st.download_button(
                label="📥 Click to Download PDF",
                data=pdf_bytes,
                file_name="sybil_report.pdf",
                mime="application/pdf"
            )

        else:
            st.markdown("---")
            st.subheader("🔒 Full Analysis & PDF Report")
            st.markdown("""
            **Upgrade to get:**
            - Full transaction analytics  
            - Gas usage charts  
            - Recent transaction logs  
            - ETH balance tracking  
            - A downloadable PDF report  
            """)
            st.link_button("🔓 Unlock Full Report ($29)", "https://your-gumroad-link.com")

    else:
        st.error("❌ Could not fetch transactions. Please try a different address.")

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

