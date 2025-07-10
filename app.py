import streamlit as st
from turtle import st
from chain_api import fetch_wallet_data
import pandas as pd

# Page config
st.set_page_config(page_title="Sybil Checker", layout="wide")

# Title and instructions
st.title("🧠 Multi-chain Sybil Wallet Checker")
st.write(
    """
    Paste a wallet address below and select a blockchain to check for suspicious activity.
    """
)

# Supported chains
chains = [
    "Ethereum",
    "BNB",
    "Polygon",
    "Arbitrum",
    "Optimism",
    "Solana",
    "Sui",
    "Near"
]

# Chain selection
selected_chain = st.selectbox("Select Blockchain", chains)

# Wallet input
wallet_address = st.text_input("Wallet Address")

# Analyze button
if st.button("🔍 Analyze Wallet") and wallet_address:
    with st.spinner("Fetching transactions..."):
        result = fetch_wallet_data(selected_chain, wallet_address)

    if result["success"]:
        txs = result["data"]

        if txs.empty:
            st.warning("No transactions found for this address.")
        else:
            # Basic stats
            st.subheader("✅ Wallet Analysis Results")
            st.metric("Wallet Age (days)", result["features"]["wallet_age_days"])
            st.metric("Average Tx Value", f"{result['features']['avg_tx_value']:.5f}")
            st.metric("Unique Receivers", result["features"]["unique_receivers"])
            st.metric("Small Transfers (<0.01)", result["features"]["small_tx_count"])
            st.metric("Average Gas Used", f"{result['features']['avg_gas_used']:.0f}")

            # Charts
            st.write("📈 Transaction Value Over Time")
            st.line_chart(txs.set_index("timeStamp")["value"])

            st.write("⛽ Gas Used Over Time")
            st.bar_chart(txs.set_index("timeStamp")["gasUsed"])

            # Table
            st.write("📋 Recent Transactions")
            st.dataframe(txs[["hash", "from", "to", "value", "gasUsed", "timeStamp"]].tail(10))

    else:
        st.error(
            f"❌ Could not fetch transactions: {result['error']}.\n\n"
            "Try a different address or check your API key."
        )

# Footer
st.markdown(
    """
    <div style='text-align: center; color: #888; margin-top: 40px; font-size: 0.9em;'>
    © 2025 Sybil Wallet Checker • Built with ❤️ by Sayan Rawl<br>
    <a href="mailto:sayanrawl7@email.com">Contact</a> |
    <a href="https://twitter.com/RawlSayan58006">Twitter</a>
    </div>
    """,
    unsafe_allow_html=True
)
