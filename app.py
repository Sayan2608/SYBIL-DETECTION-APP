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

        # If there are no transactions, auto-mark as Sybil
        if features["tx_count"] == 0:
            st.markdown(
                "<h3 style='color:red;'>Prediction: ❌ Sybil Wallet</h3>",
                unsafe_allow_html=True
            )
            st.info("This wallet has no transactions and is automatically marked as Sybil.")

            # ✅ Store result
            insert_verification(address, signature, features, "Sybil")

        else:
            # Extract feature values for manual rules
            age = features["wallet_age_days"]
            tx_count = features["tx_count"]
            small_tx = features["small_transfer_count"]
            avg_value = features["avg_tx_value"]
            contract_count = features["contract_interaction_count"]

            # Manual rule checks
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
                rule_reasons.append("Average transaction value < 0.01 ETH")

            if contract_count == 0:
                rule_sybil = True
                rule_reasons.append("No contract interactions")

            if rule_sybil:
                st.markdown(
                    f"<h3>Prediction: <span style='color:red;'>❌ Sybil Wallet (Rule-Based)</span></h3>",
                    unsafe_allow_html=True
                )
                st.warning("Reasons: " + ", ".join(rule_reasons))

                # ✅ Store result
                insert_verification(address, signature, features, "Sybil")

            else:
                # Prepare features for model
                df = pd.DataFrame([features])
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
                prediction_label = "Sybil" if prediction else "Legit"
                prediction_text = "❌ Sybil Wallet" if prediction else "✅ Legit Wallet"
                prediction_color = "red" if prediction else "green"

                st.markdown(
                    f"<h3>Prediction: <span style='color:{prediction_color};'>{prediction_text}</span></h3>",
                    unsafe_allow_html=True
                )

                # Show feature table
                st.markdown("**Behavioral Features Used in Prediction:**")
                st.dataframe(df_model.T.rename(columns={0: "Value"}))

                # ✅ Store result
                insert_verification(address, signature, features, prediction_label)

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
