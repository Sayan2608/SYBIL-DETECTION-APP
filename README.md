# 🧠 Ethereum Sybil Wallet Checker

Detect Sybil wallets in Ethereum using machine learning and wallet activity analysis.

> ⚡ Built with Python, Streamlit, and Etherscan API  
> 🧪 Powered by Random Forest ML model trained on behavioral wallet features

---

## 🚀 Try it Live
🔗 [Launch App](https://sybil-detection-app.streamlit.app)

---

## 🛠 Features

- 📊 Transaction Analysis
- 🔎 Sybil Risk Detection (ML-powered)
- 💰 ETH Balance Checker
- ⛽ Gas Metrics & Usage Charts
- 📋 Recent Transaction Table
- 🍰 Size & Gas Distribution Charts
- ✅ Clean, responsive design

---

## 📌 How It Works

The app fetches Ethereum wallet data using the Etherscan API and extracts behavioral features like:
- Wallet age
- Number of unique receivers
- Small transfer count
- Gas usage
- Average transaction value

Then it applies a trained machine learning model to classify if the wallet shows **Sybil-like behavior**.

---

## 🧪 Sample Wallets to Try

| Wallet | Risk |
|--------|------|
| `0xF977814e90dA44bFA03b6295A0616a897441aceC` | 🟢 Low |
| `0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045` | 🟢 Low |

---

## 🧰 Tech Stack

- Streamlit
- Scikit-learn
- Pandas
- Requests
- Etherscan API

---

## 📩 Contact & Social

- 💬 sayanrawl7@email.com  
- 🐦 [@RawlSayan58006](https://twitter.com/RawlSayan58006)

---

## 🤝 Support or Partnership

Looking to integrate with your crypto community or DAO?  
Interested in API access, white-label solutions, or freelance implementation?

📩 [Reach out via email](mailto:sayanrawl7@email.com)
