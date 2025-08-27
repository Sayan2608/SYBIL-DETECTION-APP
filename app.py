import streamlit as st
from wallet_component import wallet_signature
from fetch_wallet_data import fetch_wallet_data
import joblib
import pandas as pd
from db import init_db, insert_verification

# Load ML model
model = joblib.load("sybil_model.pkl")

# Page config
st.set_page_config(page_title="TrustProof", layout="centered")

# ================= CUSTOM CSS =================
st.markdown("""
    <style>
    /* Background setup with cool image */
    .stApp {
        background: url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1950&q=80") 
                    no-repeat center center fixed;
        background-size: cover;
        position: relative;
        color: #f1f5f9;
    }

    /* Semi-transparent dark overlay */
    .stApp::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        height: 100%;
        width: 100%;
        background: rgba(0, 0, 0, 0.65);
        z-index: 0;
    }

    /* Make sure content sits above overlay */
    .stApp > div {
        position: relative;
        z-index: 1;
    }

    /* Box styling */
    .box {
        background: rgba(17, 24, 39, 0.85);
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    /* Result box */
    .result-box {
        font-size: 22px;
        font-weight: bold;
        padding: 12px;
        margin-top: 15px;
        border-radius: 10px;
        background: rgba(0,0,0,0.5);
        text-align: center;
        animation: fadeIn 0.8s ease-in-out;
    }

    /* FAQ */
    .faq-box {
        background: rgba(30, 41, 59, 0.85);
        padding: 15px;
        border-radius: 10px;
        font-size: 15px;
    }

    /* Footer */
    .footer {
        text-align: center;
        font-size: 0.9em;
        color: #bbb;
        margin-top: 30px;
    }
    .footer a {
        color: #93c5fd;
        text-decoration: none;
    }
    .footer a:hover {
        text-decoration: underline;
    }

    /* Fade-in animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)


# ================== HEADER ==================
st.markdown("<h1>TrustProof</h1>", unsafe_allow_html=True)
st.markdown("<h4>Ethereum Sybil Wallet Checker</h4>", unsafe_allow_html=True)

# ================== WALLET SIGNATURE ==================
st.markdown("<div class='box'><h3>1️⃣ Connect Your Wallet</h3>", unsafe_allow_html=True)
address, signature = wallet_signature()
st.markdown("</div>", unsafe_allow_html=True)

# ================== SYBIL DETECTION ==================
if address and signature:
    st.markdown("<div class='box'><h3>2️⃣ Detection Result</h3>", unsafe_allow_html=True)
    st.success("✅ Wallet verified successfully!")
    st.write(f"Wallet Address: {address}")

    result = fetch_wallet_data(address)

    if result["success"]:
        features = result["features"]

        if features["tx_count"] == 0:
            st.markdown("<div class='result-box sybil'>❌ Sybil Wallet (No transactions)</div>", unsafe_allow_html=True)
            insert_verification(address, signature, features, "Sybil")
        else:
            rule_sybil = False
            reasons = []

            # Manual Rules
            if features["wallet_age_days"] < 30:
                rule_sybil = True; reasons.append("Wallet age < 30 days")
            if features["tx_count"] < 3:
                rule_sybil = True; reasons.append("Transaction count < 3")
            if features["small_transfer_count"] > 100:
                rule_sybil = True; reasons.append("Too many small transfers")
            if features["avg_tx_value"] < 0.01:
                rule_sybil = True; reasons.append("Average tx value < 0.01 ETH")
            if features["contract_interaction_count"] == 0:
                rule_sybil = True; reasons.append("No contract interactions")

            if rule_sybil:
                st.markdown(f"<div class='result-box sybil'>❌ Sybil Wallet</div>", unsafe_allow_html=True)
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
                emoji = "✅" if label == "Legit" else "❌"
                box_class = "legit" if label == "Legit" else "sybil"
                st.markdown(f"<div class='result-box {box_class}'>{emoji} {label} Wallet</div>", unsafe_allow_html=True)
                insert_verification(address, signature, features, label)

                st.markdown("#### Features Used:")
                st.dataframe(df_model.T.rename(columns={0: "Value"}))
    else:
        st.error(f"Error fetching data: {result['error']}")
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.warning("Please connect and sign with your wallet.")

# ================== FAQ ==================
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

# ================== FOOTER ==================
st.markdown("""
<div class="footer">
  <p>💻 <a href="mailto:sayanrawl7@email.com">Contact Developer</a> | 
  <a href="https://github.com/Sayan2608/SYBIL-DETECTION-APP" target="_blank">GitHub Repo</a></p>
  <p>© 2025 Sayan Rawl</p>
</div>
""", unsafe_allow_html=True)
