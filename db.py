import sqlite3
import json
from datetime import datetime
import os

# Initialize database and table
def init_db():
    conn = sqlite3.connect("wallet_verifications.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS verifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wallet_address TEXT,
            signature TEXT,
            features TEXT,
            prediction TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

# Insert a new verification record
def insert_verification(address, signature, features_dict, prediction_result):
    # Safely convert NumPy values to native Python types
    safe_features = {
        k: (v.item() if hasattr(v, "item") else v)
        for k, v in features_dict.items()
    }

    features_json = json.dumps(safe_features)
    timestamp = datetime.utcnow().isoformat()

    conn = sqlite3.connect("wallet_verifications.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO verifications (wallet_address, signature, features, prediction, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (address, signature, features_json, prediction_result, timestamp))
    conn.commit()
    conn.close()

# Optional: Fetch all records (for admin dashboard)
def get_all_verifications():
    conn = sqlite3.connect("wallet_verifications.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM verifications ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows
