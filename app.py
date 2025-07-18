import streamlit as st
from wallet_component import wallet_signature
from fetch_wallet_data import fetch_wallet_data
import joblib
import pandas as pd
from db import init_db, insert_verification  # ✅ NEW

# Load the trained model
model = joblib.load("sybil_model.pkl")

# Initialize the database
init_db()

# Page setup
st.set_page_config(page_title="Sybil Wallet Checker", layout="centered", page_icon="🪐")

# -------------------------
# Custom CSS for Space Theme
# -------------------------
st.markdown("""
    <style>
    body {
        background: linear-gradient(145deg, #0d1a2b, #1c2b3a);
        color: #f1f1f1;
    }
    .stApp {
        background: url("https://images.unsplash.com/photo-1531746790731-6c087fecd65a?auto=format&fit=crop&w=1050&q=80");
        background-size: cover;
        background-attachment: fixed;
        color: white;
    }
    h1, h3, h4 {
        color: #ffffff !important;
        text-shadow: 0px 0px 8px #4caf50;
    }
    .block-container {
        padding: 2rem;
        background-color: rgba(0, 0, 0, 0.65);
        border-radius: 12px;
        box-shadow: 0px 0px 15px #4caf50;
    }
    .stButton > button {
        background-color: #4caf50;
        color: white;
        border-radius: 10px;
        padding: 0.6em 2em;
        font-weight: bold;
    }
    .stDataFrame, .stAlert, .stMarkdown, .stTextInput {
        background-color: rgba(30, 30, 30, 0.8);
        border-radius: 10px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------
# Header
# -------------------------
st.markdown("""
<div style="text-align:center; padding:20px;">
  <img src="https://cdn-icons-png.flaticon.com/512/4712/4712072.png" width="100">
  <h1>🧠 Ethereum Sybil Wallet Checker</h1>
  <p>Verify your wallet and detect Sybil behavior using AI and heuristics.</p>
</div>
""", unsafe_allow_html=True)

# -------------------------
# Wallet Signature
# -------------------------
st.subheader("1️⃣ Connect Your Wallet & Sign")
address, signature = wallet_signature()

# -------------------------
# Detection Logic
# -------------------------
if address and signature:
    st.success("✅ Wallet verified successfully!")
    st.write(f"**Wallet Address:** `{address}`")

    st.subheader("2️⃣ Sybil Detection Result")
    result = fetch_wallet_data(address)

    if result["success"]:
        features = result["features"]

        if features["tx_count"] == 0:
            st.markdown("<h3 style='color:red;'>Prediction: ❌ Sybil Wallet</h3>", unsafe_allow_html=True)
            st.info("This wallet has no transactions and is automatically marked as Sybil.")
            insert_verification(address, signature, features, "Sybil")
        else:
            # Rule-based checks
            age = features["wallet_age_days"]
            tx_count = features["tx_count"]
            small_tx = features["small_transfer_count"]
            avg_value = features["avg_tx_value"]
            contract_count = features["contract_interaction_count"]

            rule_sybil = False
            rule_reasons = []

            if age < 30:
                rule_sybil = True
                rule_reasons.append("Wallet age < 30 days")
            if tx_count < 3:
                rule_sybil = True
                rule_reasons.append("Transaction count < 3")
            if small_tx > 100:
                rule_sybil = True
                rule_reasons.append("More than 100 small transfers")
            if avg_value < 0.01:
                rule_sybil = True
                rule_reasons.append("Avg tx value < 0.01 ETH")
            if contract_count == 0:
                rule_sybil = True
                rule_reasons.append("No contract interactions")

            if rule_sybil:
                st.markdown(f"<h3>Prediction: <span style='color:red;'>❌ Sybil Wallet (Rule-Based)</span></h3>", unsafe_allow_html=True)
                st.warning("Reasons: " + ", ".join(rule_reasons))
                insert_verification(address, signature, features, "Sybil")
            else:
                # ML model prediction
                df = pd.DataFrame([features])
                df_model = df[[
                    "wallet_age_days", "tx_count", "small_transfer_count",
                    "avg_tx_value", "avg_gas_used", "contract_interaction_count"
                ]]
                prediction = model.predict(df_model)[0]
                prediction_label = "Sybil" if prediction else "Legit"
                prediction_text = "❌ Sybil Wallet" if prediction else "✅ Legit Wallet"
                prediction_color = "red" if prediction else "green"

                st.markdown(
                    f"<h3>Prediction: <span style='color:{prediction_color};'>{prediction_text}</span></h3>",
                    unsafe_allow_html=True
                )
                st.markdown("**Behavioral Features Used in Prediction:**")
                st.dataframe(df_model.T.rename(columns={0: "Value"}))
                insert_verification(address, signature, features, prediction_label)
    else:
        st.error(f"Error fetching transactions: {result['error']}")
else:
    st.warning("Please connect your wallet and sign to proceed.")

# -------------------------
# Footer
# -------------------------
st.markdown("""
<hr style="margin-top:40px;">
<div style="text-align:center; font-size:0.9em;">
  <p>🔗 <a href="mailto:sayanrawl7@email.com">Contact Developer</a> | 
  <a href="https://github.com/Sayan2608/SYBIL-DETECTION-APP" target="_blank">GitHub Repository</a></p>
  <p style="color:#aaa;">&copy; 2025 Sayan Rawl. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
