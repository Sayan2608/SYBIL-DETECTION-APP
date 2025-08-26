import streamlit as st
from wallet_component import wallet_signature
from fetch_wallet_data import fetch_wallet_data
import joblib
import pandas as pd
from db import init_db, insert_verification

# Load model & initialize DB
model = joblib.load("sybil_model.pkl")
init_db()

# Page Config
st.set_page_config(page_title="TrustProof", layout="centered")

# Custom Glowing CSS Theme
st.markdown("""
<style>
body {
    background: url('https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?auto=format&fit=crop&w=1950&q=80');
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
    font-family: 'Segoe UI', sans-serif;
    color: #ffffff;
}
html, .stApp {
    background-color: rgba(10, 10, 30, 0.85);
}
h1, h2, h3, h4, p, div, label, span, li {
    color: #ffffff !important;
    text-shadow: 0 0 8px #66f9ff, 0 0 12px #a599f9;
}
.stMarkdown p, .stMarkdown span, .css-10trblm, .css-1v0mbdj {
    color: #ffffff !important;
    text-shadow: 0 0 5px #8dfcff, 0 0 10px #c9f;
}
button, .stButton>button {
    background-color: #4f46e5;
    color: white;
    border-radius: 12px;
    padding: 0.75em 1.5em;
    border: 2px solid #7c3aed;
    transition: 0.3s ease-in-out;
    text-shadow: 0 0 5px #ffffff;
}
.stButton>button:hover {
    background-color: #6d28d9;
    border-color: #a78bfa;
    box-shadow: 0 0 12px #a78bfa;
}
.box {
    background-color: rgba(255, 255, 255, 0.04);
    padding: 2rem;
    border-radius: 20px;
    margin-top: 20px;
    border: 1px solid #7c3aed;
}
.result-box {
    background-color: rgba(0, 255, 200, 0.1);
    padding: 1rem;
    border-radius: 15px;
    margin-top: 1rem;
    border: 1px solid #00ffc8;
    text-align: center;
    font-size: 1.3rem;
    font-weight: bold;
    color: white;
    text-shadow: 0 0 8px #00ffe7;
}
.faq-box {
    background-color: rgba(255, 255, 255, 0.05);
    padding: 1rem;
    border-radius: 12px;
    border: 1px solid #6666aa;
    color: #ffffff;
    text-shadow: 0 0 6px #77eaff;
}
</style>
""", unsafe_allow_html=True)

# Title + Tagline
st.markdown("""
<h1 style='text-align: center;'>🤖 TrustProof</h1>
<h4 style='text-align: center; color: #cccccc;'>Detect Sybil wallets. Build trust in your community.</h4>
<br>
""", unsafe_allow_html=True)

# Section 1: Wallet Signature
st.markdown("<div class='box'><h3>1️⃣ Connect Your Wallet</h3>", unsafe_allow_html=True)
address, signature = wallet_signature()
st.markdown("</div>", unsafe_allow_html=True)

# Section 2: Sybil Detection
if address and signature:
    st.markdown("<div class='box'><h3>2️⃣ Detection Result</h3>", unsafe_allow_html=True)
    st.success("✅ Wallet verified successfully!")
    st.write(f"Wallet Address: {address}")

    result = fetch_wallet_data(address)

    if result["success"]:
        features = result["features"]

        if features["tx_count"] == 0:
            st.markdown("<div class='result-box' style='color:red;'>❌ Sybil Wallet (No transactions)</div>", unsafe_allow_html=True)
            insert_verification(address, signature, features, "Sybil")
        else:
            rule_sybil = False
            reasons = []

            # Manual Rule Checks
            if features["wallet_age_days"] < 30:
                rule_sybil = True
                reasons.append("Wallet age < 30 days")
            if features["tx_count"] < 3:
                rule_sybil = True
                reasons.append("Transaction count < 3")
            if features["small_transfer_count"] > 100:
                rule_sybil = True
                reasons.append("Too many small transfers")
            if features["avg_tx_value"] < 0.01:
                rule_sybil = True
                reasons.append("Average tx value < 0.01 ETH")
            if features["contract_interaction_count"] == 0:
                rule_sybil = True
                reasons.append("No contract interactions")

            if rule_sybil:
                st.markdown(f"<div class='result-box' style='color:red;'>❌ Sybil Wallet</div>", unsafe_allow_html=True)
                st.warning("Rule-based Reasons: " + ", ".join(reasons))
                insert_verification(address, signature, features, "Sybil")
            else:
                df = pd.DataFrame([features])
                df_model = df[[
                    "wallet_age_days",
                    "tx_count",
                    "small_transfer_count",
                    "avg_tx_value",
                    "avg_gas_used",
                    "contract_interaction_count"
                ]]
                prediction = model.predict(df_model)[0]
                label = "Legit" if prediction == 0 else "Sybil"
                color = "cyan" if label == "Legit" else "red"
                emoji = "✅" if label == "Legit" else "❌"
                st.markdown(f"<div class='result-box' style='color:{color};'>{emoji} {label} Wallet</div>", unsafe_allow_html=True)
                insert_verification(address, signature, features, label)

                st.markdown("#### Features Used:")
                st.dataframe(df_model.T.rename(columns={0: "Value"}))
    else:
        st.error(f"Error fetching data: {result['error']}")
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.warning("Please connect and sign with your wallet.")

# Section 3: FAQ
with st.expander("❓ FAQ - Frequently Asked Questions"):
    st.markdown("""
    <div class="faq-box">
    <strong>What is a Sybil wallet?</strong><br>
    A Sybil wallet attempts to exploit airdrops or voting systems by pretending to be multiple users.

    <br><br>
    <strong>How accurate is this checker?</strong><br>
    We combine manual rules + machine learning to give a strong estimate. Not perfect, but highly useful.

    <br><br>
    <strong>How is my data used?</strong><br>
    Wallet info is only used for Sybil detection and not shared externally.
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<hr style="margin-top:30px;">
<div style="text-align:center; font-size:0.9em; color:#888;">
  <p>💻 <a href="mailto:sayanrawl7@email.com">Contact Developer</a> | 
  <a href="https://github.com/Sayan2608/SYBIL-DETECTION-APP" target="_blank">GitHub Repo</a></p>
  <p>© 2025 Sayan Rawl — Powered by TrustProof</p>
</div>
""", unsafe_allow_html=True)
