import streamlit as st
from streamlit_js_eval import streamlit_js_eval

def wallet_signature(message="Verify ownership for Sybil detection"):
    st.markdown("### 🔐 Sign Message with MetaMask")
    st.markdown("Click the button below to connect your wallet and sign the message.")

    code = f"""
    async function connectAndSign() {{
      if (typeof window.ethereum === "undefined") {{
        return {{ error: "MetaMask not found" }};
      }}

      const accounts = await window.ethereum.request({{ method: 'eth_requestAccounts' }});
      const account = accounts[0];

      const message = `{message}`;
      const signature = await window.ethereum.request({{
        method: "personal_sign",
        params: [message, account],
      }});

      return {{
        address: account,
        signature: signature
      }};
    }}
    connectAndSign();
    """

    result = streamlit_js_eval(js_expressions=code, key="wallet_sign", want_output=True)

    if isinstance(result, dict) and "address" in result and "signature" in result:
        return result["address"], result["signature"]
    return None, None

