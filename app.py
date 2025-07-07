import streamlit as st
import pandas as pd
import requests
import joblib
from datetime import datetime

st.set_page_config(page_title="Sybil Wallet Checker", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    body {
        background-color: #f9f9f9;
    }
    h1, h2, h3 {
        color: #4CAF50;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 6px;
        padding: 0.5em 1.2em;
        font-weight: 600;
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
    unsafe_allow_html=True,
)

st.title("🧠 Ethereum Sybil Wallet Checker")
st.write("Enter an Ethereum wallet address to get a free basic Sybil risk screening.")

wallet_address = st.text_input("🔗 **Ethereum Wallet Address**")

model = joblib.load("sybil_model.pkl")

if st.button("🔍 Analyze Wallet") and wallet_address:
    with st.spinner("Fetching data from Etherscan..."):
        tx_url = (
            f"https://api.etherscan.io/api"
            f"?module=account&action=txlist"
            f"&address={wallet_address}"
            f"&startblock=0&endblock=99999999&sort=asc"
            f"&apikey={st.secrets['api']['etherscan']}"
        )
        tx_response = requests.get(tx_url)

    if tx_response.status_code == 200:
        tx_data = tx_response.json()
        if tx_data["status"] == "1" and tx_data["result"]:
            txs = pd.DataFrame(tx_data["result"])
            txs["value"] = txs["value"].astype(float) / 1e18
            txs["gasUsed"] = txs["gasUsed"].astype(float)
            txs["timeStamp"] = pd.to_datetime(txs["timeStamp"], unit="s")

            # Basic metrics
            wallet_age_days = (pd.Timestamp.now() - txs["timeStamp"].min()).days
            avg_tx_value = txs["value"].mean()

            # Compute minimal features for prediction
            features = pd.DataFrame([{
                "wallet_age_days": wallet_age_days,
                "unique_receivers": txs["to"].nunique(),
                "avg_tx_value": avg_tx_value,
                "small_tx_count": (txs["value"] < 0.01).sum(),
                "avg_gas_used": txs["gasUsed"].mean()
            }])

            prediction = model.predict(features)[0]

            # Show free results
            st.subheader("✅ Basic Free Results")
            col1, col2 = st.columns(2)
            col1.metric("Wallet Age", f"{wallet_age_days} days")
            col2.metric("Average Tx Value", f"{avg_tx_value:.5f} ETH")

            if prediction == 1:
                st.error("🔴 High Sybil Risk detected.")
            else:
                st.success("🟢 Low Sybil Risk detected.")

            # Paid content notice
            st.markdown("---")
            st.subheader("🔒 Full Analysis & PDF Report")
            st.write("""
            Upgrade to get:
            - Full transaction analytics
            - Gas usage charts
            - Recent transaction logs
            - ETH balance tracking
            - A downloadable PDF report
            """)
            st.markdown(
                """
                <a href="https://sayanrawl.gumroad.com/l/rhvdu" target="_blank">
                    <button style="background:#FF6F61;color:white;border:none;padding:0.8em 1.5em;border-radius:6px;font-size:1em;font-weight:600;cursor:pointer;">
                        🔓 Unlock Full Report ($29)
                    </button>
                </a>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning("⚠️ No transactions found or invalid wallet.")
    else:
        st.error("❌ Failed to fetch data from Etherscan.")

# Footer
st.markdown(
    """
    <div class="footer">
        © 2025 Sybil Wallet Checker • Built with ❤️ by Sayan Rawl <br>
        <a href="mailto:sayanrawl7@email.com">Contact</a> |
        <a href="https://twitter.com/RawlSayan58006" target="_blank">Twitter</a>
    </div>
    """,
    unsafe_allow_html=True
)
