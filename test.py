import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="Test Wallet")
st.title("🔑 Wallet Connect Test")

address = streamlit_js_eval(
    js_code="""
        async () => {
            if (typeof window.ethereum === "undefined") {
                return "No wallet found";
            }
            await window.ethereum.request({ method: 'eth_requestAccounts' });
            const accounts = await ethereum.request({ method: 'eth_accounts' });
            return accounts[0];
        }
    """,
    key="wallet_connect_test",
    label="wallet_connect_test",  # ✅ Important line!
)

if address:
    st.success(f"✅ Connected: {address}")
else:
    st.warning("⚠️ No wallet connected.")
