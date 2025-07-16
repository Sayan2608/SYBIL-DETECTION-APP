import streamlit as st
from streamlit import streamlit_js_eval # type: ignore

st.title("🔑 Wallet Signature Test")

signed = streamlit_js_eval(
    js_expressions=[
        """
        (async () => {
            if (!window.ethereum) {
                return {error: "No wallet detected"};
            }
            const accounts = await window.ethereum.request({ method: "eth_requestAccounts" });
            const address = accounts[0];
            const message = "Verify ownership for Sybil detection";
            const signature = await window.ethereum.request({
                method: "personal_sign",
                params: [message, address]
            });
            return {address, message, signature};
        })()
        """
    ],
    key="signer",
)

st.write("Signature Response:")
st.json(signed)
