import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Admin Dashboard", layout="wide")
st.title("🛡️ Admin Dashboard - Sybil Wallet Verifications")

ADMIN_CODE = "260804"
passcode = st.text_input("Enter Admin Passcode", type="password")

if passcode != ADMIN_CODE:
    st.warning("Access restricted. Please enter the correct passcode.")
    st.stop()

st.success("✅ Access granted!")

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
