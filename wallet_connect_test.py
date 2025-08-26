import streamlit as st
from streamlit_js_eval import streamlit_js_eval 

# Set up Streamlit page
st.set_page_config(page_title="Wallet Connect Test", layout="centered")
st.title("🔑 Wallet Connect Test")

st.write(
    """
    This is a minimal test to verify that `streamlit_js_eval` can access MetaMask.
    When you open this page, it will try to connect to your wallet automatically.
    """
)


# Run JavaScript to request wallet connection
address = streamlit_js_eval(
    """
    async () => {
        if (typeof window.ethereum === "undefined") {
            return "No wallet found";
        }
        await window.ethereum.request({ method: 'eth_requestAccounts' });
        const accounts = await ethereum.request({ method: 'eth_accounts' });
        return accounts[0];
    }
    """
)

# Display the result
if address:
    if address == "No wallet found":
        st.error("❌ No Ethereum wallet detected. Please install MetaMask.")
    else:
        st.success(f"✅ Connected wallet: {address}")
