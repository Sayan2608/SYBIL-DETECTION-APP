import streamlit as st
from streamlit.components.v1 import html
from wallet_component import wallet_signature # type: ignore
from fetch_wallet_data import fetch_wallet_data # type: ignore
import joblib
import pandas as pd
from db import insert_verification # type: ignore
import warnings

# ============ APP INIT ============
st.set_page_config(page_title="TrustProof", layout="centered")
st.title("✅ TrustProof Sybil Detection App")

# ============ WARNINGS ============
warnings.filterwarnings("ignore")  # Optional: Hides the sklearn version warning

# ============ LOAD MODEL WITH DEBUG ============
@st.cache_resource
def load_model():
    try:
        model = joblib.load("sybil_model.pkl")
        return model
    except Exception as e:
        st.error(f"❌ Model loading failed: {e}")
        return None

model = load_model()

if model is not None:
    st.success("✅ ML model loaded successfully")
else:
    st.stop()  # Stop app if model is not loaded

# ============ HEADER ============
st.markdown("<h1>TrustProof</h1>", unsafe_allow_html=True)
st.markdown("<h4>Ethereum Sybil Wallet Checker</h4>", unsafe_allow_html=True)

# ============ STEP 1: Wallet Signature ============
st.markdown("<div class='box'><h3>1️⃣ Connect Your Wallet</h3>", unsafe_allow_html=True)

try:
    address, signature = wallet_signature()
    st.success("✅ Wallet loaded")
except Exception as e:
    st.error(f"❌ Wallet signature error: {e}")
    address = None
    signature = None

st.markdown("</div>", unsafe_allow_html=True)

# ============ STEP 2: Detection Logic ============
if address and signature:
    st.markdown("<div class='box'><h3>2️⃣ Detection Result</h3>", unsafe_allow_html=True)
    st.write(f"🔗 Wallet Address: {address}")

    result = fetch_wallet_data(address)

    if result["success"]:
        features = result["features"]

        if features["tx_count"] == 0:
            st.markdown("<div class='result-box sybil'>❌ Sybil Wallet (No transactions)</div>", unsafe_allow_html=True)
            insert_verification(address, signature, features, "Sybil")
        else:
            rule_sybil = False
            reasons = []

            # ----- Manual Rule Check -----
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
                # ----- ML Model Prediction -----
                df = pd.DataFrame([features])
                df_model = df[[
                    "wallet_age_days",
                    "tx_count",
                    "small_transfer_count",
                    "avg_tx_value",
                    "avg_gas_used",
                    "contract_interaction_count"
                ]]
                try:
                    prediction = model.predict(df_model)[0]
                    label = "Legit" if prediction == 0 else "Sybil"
                    emoji = "✅" if label == "Legit" else "❌"
                    box_class = "legit" if label == "Legit" else "sybil"
                    st.markdown(f"<div class='result-box {box_class}'>{emoji} {label} Wallet</div>", unsafe_allow_html=True)
                    insert_verification(address, signature, features, label)

                    st.markdown("#### Features Used:")
                    st.dataframe(df_model.T.rename(columns={0: "Value"}))
                except Exception as e:
                    st.error(f"❌ ML prediction error: {e}")

    else:
        st.error(f"❌ Error fetching wallet data: {result['error']}")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.warning("⚠️ Please connect and sign with your wallet to continue.")

# ============ FAQ SECTION ============
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

# ============ FOOTER ============
st.markdown("""
<div class="footer">
  <p>💻 <a href="mailto:sayanrawl7@email.com">Contact Developer</a> | 
  <a href="https://github.com/Sayan2608/SYBIL-DETECTION-APP" target="_blank">GitHub Repo</a></p>
  <p>© 2025 Sayan Rawl</p>
</div>
""", unsafe_allow_html=True)

# ============ CUSTOM CSS ============
st.markdown("""
<style>
/* Background */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Headings */
h1 {
    color: #FFD700;
    text-align: center;
    font-size: 42px !important;
}
h4 {
    color: #87CEEB;
    text-align: center;
}

/* Box styling */
.box {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 15px;
    margin: 15px 0;
}

/* Result styles */
.result-box {
    text-align: center;
    padding: 15px;
    border-radius: 12px;
    font-size: 20px;
    margin: 15px 0;
    font-weight: bold;
}
.result-box.legit {
    background: #4CAF50;
    color: white;
}
.result-box.sybil {
    background: #FF4C4C;
    color: white;
}

/* FAQ box */
.faq-box {
    background: rgba(255, 255, 255, 0.15);
    border-radius: 12px;
    padding: 12px;
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 30px;
    font-size: 14px;
    color: #ccc;
}
.footer a {
    color: #FFD700;
    text-decoration: none;
}
.footer a:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)
