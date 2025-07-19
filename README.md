# 🧠 Ethereum Sybil Wallet Checker

A Sybil detection tool that analyzes any Ethereum wallet using both rule-based logic and a machine learning model. Built to help DAOs, airdrop campaigns, and web3 communities fight Sybil attacks.

👉 [Try the App](https://sybil-wallet-checker.streamlit.app/)

## 🔍 Features

- 🦊 Connect via MetaMask
- ✍️ Wallet signature authentication
- 📊 Real-time Sybil analysis
- 🧠 Rule-based + ML detection
- 🎨 Space-themed, futuristic UI
- 📁 Admin dashboard to manage wallet entries

## 🧪 How It Works

1. User connects their Ethereum wallet.
2. The app fetches wallet data (age, tx count, gas usage, etc.)
3. Applies rule-based filters (e.g. new wallet, no txs = likely Sybil)
4. If passed, ML model makes final prediction
5. Result shown + saved to backend for admins

## 🔐 Built For

- DAOs & governance communities
- Airdrop and retroactive funding programs
- NFT mints and whitelists
- Web3 teams dealing with Sybil abuse

## ⚙️ Tech Stack

- 🐍 Python
- 📦 Streamlit
- 🤖 Scikit-learn ML
- 📡 Ethereum JSON-RPC
- 📁 Local DB (CSV/JSON, easily replaceable with SQL)
- 🎨 Custom CSS styling

## 📚 Folder Structure

```
📁 SybilWalletChecker/
│
├── app.py              # Main Streamlit app
├── admin.py            # Admin dashboard for reviewing results
├── fetch_wallet_data.py# Ethereum wallet data parser
├── train_model.py      # ML model training
├── sybil_model.pkl     # Saved trained ML model
├── assets/             # Images, robot mascot, backgrounds
└── README.md           # Project documentation
```

## 🏛️ Looking for Support

I'm currently seeking:
- DAO or protocol partnerships
- Grant or retro funding opportunities
- Feedback from web3 security researchers

If you're part of a DAO or web3 project impacted by Sybil attacks, let’s collaborate!

📧 Contact: sayanrawl.eth@proton.me  
🐦 Twitter: [@your_handle]()

---

## 💻 Run Locally

```bash
git clone https://github.com/sayanrawl/SybilWalletChecker.git
cd SybilWalletChecker
pip install -r requirements.txt
streamlit run app.py
```

---

## 🛠️ Coming Soon

- 💾 Full SQL + IPFS/Arweave data storage
- 🧬 Sybil scoring instead of binary labels
- 📑 PDF reports export
- 🔗 Multi-chain support (ZKSync, Arbitrum, Base)
