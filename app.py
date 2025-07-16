# app.py
import streamlit as st
import pandas as pd
import joblib
from fetch_wallet_data import fetch_wallet_data
import json

# Load ML model
model = joblib.load("sybil_model.pkl")

# Page configuration
st.set_page_config(
    page_title="Ethereum Sybil Wallet Checker",
    layout="wide",
    page_icon="🧠"
)

# --- Header ---
st.markdown("""
<div style="text-align: center;">
    <h1>🧠 Ethereum Sybil Wallet Checker</h1>
    <p style="font-size:1.1em;">
        Verify ownership of your wallet and detect potential Sybil activity instantly.
    </p>
</div>
""", unsafe_allow_html=True)

st.write("---")

# --- Wallet Connect Section ---
st.subheader("1️⃣ Connect Your Wallet & Sign Message")

st.markdown("Click the button below to connect your MetaMask wallet and sign a message.")

# Embed HTML + JavaScript to connect and sign
html_code = """
<!DOCTYPE html>
<html>
  <body>
    <button onclick="connectAndSign()" style="padding:0.6em 1.2em; font-size:1em;">🔑 Connect & Sign</button>
    <p id="output" style="font-family:monospace; font-size:0.9em;"></p>
    <script>
      async function connectAndSign() {
        if (typeof window.ethereum === 'undefined') {
          document.getElementById("output").textContent = "MetaMask not detected.";
          return;
        }
        await ethereum.request({ method: 'eth_requestAccounts' });
        const accounts = await ethereum.request({ method: 'eth_accounts' });
        const account = accounts[0];
        const message = "Verify ownership of this wallet for Sybil analysis.";
        const signature = await ethereum.request({
          method: "personal_sign",
          params: [message, account]
        });
        const result = {
          account: account,
          signature: signature
        };
        const json = JSON.stringify(result);
        const textarea = document.createElement("textarea");
        textarea.value = json;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand("copy");
        document.body.removeChild(textarea);
        document.getElementById("output").textContent = "✅ Wallet connected and signature copied to clipboard. Paste it into the field below.";
      }
    </script>
  </body>
</html>
"""

# Display the HTML
st.components.v1.html(html_code, height=180)

# Text input to paste the JSON
st.write("Paste the copied JSON here:")
signed_json = st.text_area("Wallet Signature JSON")

if signed_json.strip():
    try:
        parsed = json.loads(signed_json)
        wallet_address = parsed["account"]
        signature = parsed["signature"]

        st.success(f"✅ Wallet Connected: `{wallet_address}`")
        with st.expander("🔍 View Signed Message Details"):
            st.code("Verify ownership of this wallet for Sybil analysis.", language="text")
            st.code(signature, language="text")

        # --- Sybil Detection Section ---
        st.subheader("2️⃣ Sybil Detection Results")
        with st.spinner("Fetching wallet data and running prediction..."):
            result = fetch_wallet_data(wallet_address)
            if result["success"]:
                features = result["features"]

                st.markdown("### 📊 Wallet Metrics")
                col1, col2, col3 = st.columns(3)
                col1.metric("Wallet Age (days)", features["wallet_age_days"])
                col1.metric("Transaction Count", features["tx_count"])
                col1.metric("Unique Receivers", features["unique_receivers"])
                col2.metric("Avg Tx Value (wei)", f"{features['avg_tx_value']:.2f}")
                col2.metric("Avg Gas Used", f"{features['avg_gas_used']:.2f}")
                col3.metric("Contract Interactions", features["contract_interaction_count"])

                if features["is_sybil_no_transactions"]:
                    st.warning("⚠️ No transactions found. Marked as Sybil by default.")
                else:
                    input_features = pd.DataFrame([[
                        features["wallet_age_days"],
                        features["tx_count"],
                        features["small_transfer_count"],
                        features["avg_tx_value"],
                        features["avg_gas_used"],
                        features["contract_interaction_count"]
                    ]])
                    prediction = model.predict(input_features)[0]
                    if prediction == 1:
                        st.error("❌ This wallet is likely a **Sybil wallet**.")
                    else:
                        st.success("✅ This wallet does **not appear to be Sybil**.")
            else:
                st.error(f"Error fetching wallet data: {result['error']}")

    except Exception as e:
        st.error(f"Invalid JSON pasted. {e}")

# --- Footer ---
st.write("---")
st.markdown("""
<div style="text-align: center; font-size:0.9em; color: #666;">
    Built with ❤️ using Streamlit · 
    <a href="mailto:sayanrawl7@email.com" target="_blank">Contact Developer</a> · 
    <a href="https://github.com/" target="_blank">GitHub</a>
</div>
""", unsafe_allow_html=True)
