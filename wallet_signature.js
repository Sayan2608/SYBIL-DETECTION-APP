const streamlitComponent = window.parent;

function sendData(data) {
  streamlitComponent.postMessage(
    {
      isStreamlitMessage: true,
      type: "streamlit:setComponentValue",
      value: data,
    },
    "*"
  );
}

window.addEventListener("message", async (event) => {
  if (!event.data || event.data.type !== "SIGN_REQUEST") return;

  if (typeof window.ethereum === "undefined") {
    sendData({ error: "No wallet detected. Please install MetaMask." });
    return;
  }

  try {
    await window.ethereum.request({ method: "eth_requestAccounts" });
    const accounts = await ethereum.request({ method: "eth_accounts" });
    const account = accounts[0];

    const message = event.data.message;
    const signature = await ethereum.request({
      method: "personal_sign",
      params: [message, account],
    });

    sendData({
      address: account,
      signature: signature,
      message: message,
    });
  } catch (err) {
    sendData({ error: err.message });
  }
});
