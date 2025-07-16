import streamlit as st
from wallet_component import wallet_signature
from fetch_wallet_data import fetch_wallet_data
import joblib
import pandas as pd

# Load the trained model
model = joblib.load("sybil_model.pkl")

st.set_page_config(page_title="Sybil Wallet Checker", layout="centered")

# ------------------------------
# Header
# ------------------------------
st.markdown("""
<div style="text-align:center; padding:20px 0;">
  <h1 style="color:#4CAF50;">🧠 Ethereum Sybil Wallet Checker</h1>
  <p>Verify ownership of your wallet and detect potential Sybil activity instantly.</p>
</div>
""", unsafe_allow_html=True)

# ------------------------------
# Wallet Signature
# ------------------------------
st.subheader("1️⃣ Connect Your Wallet & Sign")
address, signature = wallet_signature()

# ------------------------------
# Detection Logic
# ------------------------------
if address and signature:
    st.success("✅ Wallet verified successfully!")
    st.write(f"**Wallet Address:** `{address}`")

    # Fetch wallet data
    st.subheader("2️⃣ Sybil Detection Result")
    result = fetch_wallet_data(address)

    if result["success"]:
        features = result["features"]
        df = pd.DataFrame([features])

        # Prepare features for model
        df_model = df[[
            "wallet_age_days",
            "tx_count",
            "small_transfer_count",
            "avg_tx_value",
            "avg_gas_used",
            "contract_interaction_count"
        ]]

        # Predict
        prediction = model.predict(df_model)[0]
        prediction_text = "🛑 Sybil Detected" if prediction else "✅ Legit Wallet"
        prediction_color = "red" if prediction else "green"

        st.markdown(
            f"<h3>Prediction: <span style='color:{prediction_color};'>{prediction_text}</span></h3>",
            unsafe_allow_html=True
        )

        # Show feature table
        st.markdown("**Behavioral Features Used in Prediction:**")
        st.dataframe(df_model.T.rename(columns={0: "Value"}))
    else:
        st.error(f"Error fetching transactions: {result['error']}")
else:
    st.warning("Please connect your wallet and sign the message to proceed.")

# ------------------------------
# Footer
# ------------------------------
st.markdown("""
<hr style="margin-top:40px;">
<div style="text-align:center; font-size:0.9em;">
  <p>🔗 <a href="mailto:sayanrawl7@email.com">Contact Developer</a> | 
  <a href="https://github.com/Sayan2608/SYBIL-DETECTION-APP" target="_blank">GitHub Repository</a></p>
  <p style="color:#888;">&copy; 2025 Sayan Rawl. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)

