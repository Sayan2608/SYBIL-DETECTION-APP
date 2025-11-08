# 🧠 Ethereum Sybil Wallet Checker

A Sybil detection tool that analyzes any Ethereum wallet using both rule-based logic and a machine learning model.  
Built to help DAOs, airdrop campaigns, and web3 communities fight Sybil attacks.

👉 [Try the Live App](https://sybil-detection-app-4yrprxrpg5ln6rzpyvh5sy.streamlit.app/)  
👉 [Landing Page](https://github.com/Sayan2608/sybil-landing-page)

---

## 🔍 Features

- 🦊 Connect via MetaMask
- ✍️ Wallet signature authentication
- 📊 Real-time Sybil detection
- 🧠 Rule-based + ML classification
- 🎨 Space-themed, futuristic UI
- 🔐 Admin dashboard to manage verified wallets

---

## 🧪 How It Works

1. User connects their Ethereum wallet and signs a message.
2. The app fetches wallet data (wallet age, tx count, gas usage, etc.)
3. Rule-based filters are applied (e.g. new wallet, 0 txs = likely Sybil)
4. If passed, an ML model makes the final prediction
5. Result is shown + saved to the backend (for DAO admins)

---

## 🎯 Built For

- DAOs & governance platforms
- Airdrop and retro funding programs
- NFT allowlists and launchpads
- Web3 teams battling Sybil attacks

---

## ⚙️ Tech Stack

- 🐍 Python
- 📦 Streamlit
- 🤖 Scikit-learn (ML model)
- 📡 Ethereum RPC / Etherscan API
- 💽 SQLite (or CSV as fallback)
- 🎨 Custom CSS + JS wallet injection

---

## 📁 Folder Structure

```
📁 SybilWalletChecker/
│
├── app.py               # Main app UI
├── admin.py             # Admin dashboard for DAO teams
├── fetch_wallet_data.py # On-chain feature extractor
├── train_model.py       # ML model training
├── sybil_model.pkl      # Trained classifier
├── db.py                # Database handler (SQLite)
├── wallet_component.py  # MetaMask wallet connector
├── assets/              # Backgrounds, robot images
└── README.md
```

---

## 🧠 Future Roadmap

- 💾 SQL + IPFS/Arweave support
- 🔢 Sybil score (0-100) instead of binary label
- 📄 Export PDF reports
- 🌐 Multi-chain support (ZKSync, Arbitrum, Base, StarkNet)

---

## 🏛️ Seeking Partners

We’re actively looking for:
- DAO & protocol partners
- Web3 grants or retroactive funding
- Feedback from Sybil attack victims

📧 sayanrawl.eth@proton.me  
🐦 Twitter: https://x.com/RawlSayan58006?s=09

---

## 💻 Run Locally

```bash
git clone https://github.com/Sayan2608/SYBIL-DETECTION-APP
cd SYBIL-DETECTION-APP
pip install -r requirements.txt
streamlit run app.py
```

---

⭐ Star this repo if you support Sybil-resistance tools for Web3.
