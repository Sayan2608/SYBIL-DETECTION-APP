import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Admin Dashboard", layout="wide", page_icon="🛡️")

# -------------------------
# Space-Themed Styling
# -------------------------
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(145deg, #101928, #1c2b3a);
        color: white;
    }
    .block-container {
        padding: 2rem;
        background-color: rgba(0, 0, 0, 0.65);
        border-radius: 12px;
        box-shadow: 0px 0px 15px #6c5ce7;
    }
    .stButton > button {
        background-color: #6c5ce7;
        color: white;
        font-weight: bold;
        border-radius: 10px;
    }
    h1, h2, h3 {
        color: #ffffff !important;
        text-shadow: 0px 0px 8px #6c5ce7;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------
# Authentication
# -------------------------
st.title("🛡️ Admin Dashboard - Sybil Wallet Verifications")

ADMIN_CODE = "260804"
passcode = st.text_input("Enter Admin Passcode", type="password")

if passcode != ADMIN_CODE:
    st.warning("Access restricted. Please enter the correct passcode.")
    st.stop()

st.success("✅ Access granted!")

# -------------------------
# Load Verification Records
# -------------------------
conn = sqlite3.connect("wallet_verifications.db")
cursor = conn.cursor()

try:
    df = pd.read_sql_query("SELECT * FROM verifications ORDER BY timestamp DESC", conn)

    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        st.markdown("### ✅ Verified Wallets Data")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name='wallet_verifications.csv',
            mime='text/csv'
        )
    else:
        st.info("No verification records yet.")
except Exception as e:
    st.error(f"Error fetching data: {e}")

conn.close()

